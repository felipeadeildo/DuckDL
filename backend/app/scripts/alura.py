from bs4 import BeautifulSoup

from .base.node import Node
from .base.platform import PlatformDownloader


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
            await self.log("login_error")
            await self.account_service.set_account_status(self.account.id, "error")
            self.is_logged = False
        else:
            await self.log("login_success")
            self.is_logged = True

    async def _list_products(self):
        if not self.is_logged:
            await self._login()

        if not self.is_logged:
            return

        await self.__get_products()
        await self.account_service.set_account_status(
            self.account.id, "products_listed"
        )

    async def __get_products(self) -> list[AluraNode]:
        soup = await self.get_soup(self.session.get, f"{self.BASE_URL}/courses")

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
                self.session.get, f"{self.BASE_URL}/{next_page.get('href')}"
            )

        await self.log("account_products_listed_success", count=len(products))

        return products

    async def map_product(self, node: ...): ...

    async def start_download(self, node: ...): ...
