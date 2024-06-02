from app.scripts.base.node import Node
from app.scripts.base.utils import get_soup, valid_tag


class AluraNode(Node):
    BASE_URL = "https://cursos.alura.com.br"

    async def download(self):
        await self.load_children()

        for child in self.children:
            await child.download()

        if self.type == "lesson":
            await self.__download_lesson()
        else:
            await self.log("node_success_downloaded")
            await self.node_service.set_status(self.id, "downloaded")

    async def _load_children(self):
        loaders = {
            "course": self.__load_modules,
            "module": self.__load_lessons,
        }

        loader = loaders.get(self.type)
        if not loader:
            return

        await self.log("node_start_mapping_children")
        await self.node_service.set_status(self.id, "mapping")
        await loader()

    async def __load_modules(self):
        soup = await get_soup(self.session.get, self.url)

        module_tags = soup.find_all("li", {"class": "courseSection-listItem"})

        for i, module_tag in enumerate(module_tags, 1):
            name_tag = valid_tag(
                module_tag.find("div", {"class": "courseSectionList-sectionTitle"})
            )

            if not name_tag:
                await self.log("node_name_not_found", order=i, node_type="module")
                name = "Módulo"
            else:
                for object_tag in name_tag.find_all("object"):
                    object_tag.decompose()
                name = name_tag.get_text(strip=True)

            module = {
                "name": name,
                "type": "module",
                "order": i,
                "url": f"{self.BASE_URL}{module_tag.a.get('href')}",
                **self.NODE_DEFAULTS,
            }
            node = AluraNode(**module)
            await node.flush_node_db()
            self.children.append(node)

        await self.node_service.set_status(self.id, "mapped")
        await self.log(
            "node_success_mapped", count=len(self.children), children_type="module"
        )

    async def __load_lessons(self):
        soup = await get_soup(self.session.get, self.url)

        lesson_tags = soup.find_all("li", {"class": "task-menu-nav-item"})

        for i, lesson_tag in enumerate(lesson_tags, 1):
            name_tag = valid_tag(
                lesson_tag.find("span", {"class": "task-menu-nav-item-title"})
            )

            if not name_tag:
                await self.log("node_name_not_found", node_type="lesson", order=i)
                name = "Aula"
            else:
                name = name_tag.get("title")

            lesson = {
                "name": name,
                "type": "lesson",
                "url": f"{self.BASE_URL}{lesson_tag.a.get('href')}",
                **self.NODE_DEFAULTS,
            }
            node = AluraNode(**lesson)
            await node.flush_node_db()
            self.children.append(node)

        await self.node_service.set_status(self.id, "mapped")
        await self.log(
            "node_success_mapped", count=len(self.children), children_type="lesson"
        )

    async def __download_lesson(self):
        await self.log("node_start_download")
        await self.node_service.set_status(self.id, "downloading")

        await self.node_service.set_status(self.id, "downloaded")
        await self.log("node_success_downloaded")
