from bs4 import BeautifulSoup

from .base import PlatformDownloader


class AluraDownloader(PlatformDownloader):
    BASE_URL = "https://cursos.alura.com.br"

    async def _login(self):
        self._create_session()
        self.session.get(f"{self.BASE_URL}/loginForm")

        res = self.session.post(
            f"{self.BASE_URL}/loginForm",
            data={"username": self.account.username, "password": self.account.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        soup = BeautifulSoup(res.content, "html.parser")

        if not soup.find("div", {"class": "user-name"}):
            await self.logger.error(
                "Falha ao fazer login, verifique as credenciais.",
                account_id=self.account.id,
            )
            self.is_logged = False
        else:
            self.is_logged = True

        await self.logger.debug(
            "Login efetuado com sucesso.", account_id=self.account.id
        )

    async def list_products(self):
        if not self.is_logged:
            await self._login()

        if not self.is_logged:
            return
