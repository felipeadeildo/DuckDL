from bs4 import BeautifulSoup
from fastapi.concurrency import run_in_threadpool

from .base import NodeBase, PlatformDownloader


class AluraNode(NodeBase):
    async def download(self): ...

    async def load_children(self): ...


class AluraDownloader(PlatformDownloader):
    BASE_URL = "https://cursos.alura.com.br"

    async def _login(self):
        self._create_session()

        await run_in_threadpool(self.session.get, f"{self.BASE_URL}/loginForm")

        res = await run_in_threadpool(
            self.session.post,
            f"{self.BASE_URL}/signin",
            data={"username": self.account.username, "password": self.account.password},
        )

        soup = BeautifulSoup(res.content, "html.parser")

        if not soup.find("button", {"class": "user-name"}):
            await self.log_service.error(
                "Falha ao fazer login, verifique as credenciais.",
                account_id=self.account.id,
            )
            self.is_logged = False
        else:
            await self.log_service.debug(
                "Login efetuado com sucesso!", account_id=self.account.id
            )
            self.is_logged = True

    async def list_products(self):
        current_status = await self.account_service.get_account_status(self.account.id)
        if current_status != "stopped":
            return

        await self.account_service.set_account_status(
            self.account.id, "listing_products"
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
        soup = await run_in_threadpool(
            self.get_soup, self.session.get, f"{self.BASE_URL}/courses"
        )

        products = []
        while True:
            course_cards = soup.find_all("li", {"class": "card-list__item"})
            for course_card in course_cards:
                course = {
                    "name": course_card.get("data-course-name"),
                    "type": "course",
                    "url": f"{self.BASE_URL}/{course_card.a.get('href')}",
                    "session": self.session,
                    "prisma": self.prisma,
                }
                products.append(AluraNode(**course))

            next_page = self.valid_tag(
                soup.find("a", {"class": "busca-paginacao-linksProximos"})
            )
            if not next_page:
                break
            soup = await run_in_threadpool(
                self.get_soup,
                self.session.get,
                f"{self.BASE_URL}/{next_page.get('href')}",
            )

        await self.log_service.debug(
            f"Encontrados {len(products)} cursos na conta.", account_id=self.account.id
        )

        return products

    async def map_product(self, node: ...): ...

    async def start_download(self, node: ...): ...
