from bs4 import BeautifulSoup

from .base.node import Node
from .base.platform import PlatformDownloader

# TODO: Move all the log_service method calls to methods of the Node (abstract)


class AluraNode(Node):
    async def download(self): ...

    async def load_children(self): ...


class AluraDownloader(PlatformDownloader):
    BASE_URL = "https://cursos.alura.com.br"

    async def _login(self):
        self._create_session()

        await self.session.get(f"{self.BASE_URL}/loginForm")

        res = await self.session.post(
            f"{self.BASE_URL}/signin",
            data={"username": self.account.username, "password": self.account.password},
        )

        soup = BeautifulSoup(res.content, "html.parser")

        if not soup.find("button", {"class": "user-name"}):
            await self.log_service.error(
                "Falha ao fazer login, verifique as credenciais.",
                account_id=self.account.id,
            )
            await self.account_service.set_account_status(self.account.id, "error")
            self.is_logged = False
        else:
            await self.log_service.debug(
                "Login efetuado com sucesso!", account_id=self.account.id
            )
            self.is_logged = True

    async def list_products(self):
        current_status = await self.account_service.get_account_status(self.account.id)
        if current_status not in ("stopped", "error", "products_listed"):
            await self.log_service.error(
                f"A conta encontra-se em um status que impede a listagem de produtos: {current_status}",
                account_id=self.account.id,
            )
            return

        if current_status == "products_listed":
            await self.account_service.delete_products(self.account.id)
            await self.log_service.info(
                "Produtos removidos para reiniciar a listagem",
                account_id=self.account.id,
            )

        await self.account_service.set_account_status(
            self.account.id, "listing_products"
        )

        await self.log_service.debug(
            "Iniciando a lisgem de produtos.",
            account_id=self.account.id,
        )

        if not self.is_logged:
            await self._login()

        if not self.is_logged:
            return

        await self.__list_products()
        await self.account_service.set_account_status(
            self.account.id, "products_listed"
        )

    async def __list_products(self) -> list[AluraNode]:
        soup = await self.get_soup(self.session.get, f"{self.BASE_URL}/courses")

        products = []
        while True:
            course_cards = soup.find_all("li", {"class": "card-list__item"})
            for course_card in course_cards:
                course = {
                    "name": course_card.get("data-course-name"),
                    "type": "course",
                    "url": f"{self.BASE_URL}{course_card.a.get('href')}",
                    "session": self.session,
                    "prisma": self.prisma,
                    "account": self.account,
                }
                node = AluraNode(**course)
                await node.flush_node_db()
                products.append(node)

            next_page = self.valid_tag(
                soup.find("a", {"class": "busca-paginacao-linksProximos"})
            )
            if not next_page:
                break

            soup = await self.get_soup(
                self.session.get, f"{self.BASE_URL}{next_page.get('href')}"
            )

        await self.log_service.debug(
            f"Encontrados {len(products)} cursos na conta.", account_id=self.account.id
        )

        return products

    async def map_product(self, node: ...): ...

    async def start_download(self, node: ...): ...
