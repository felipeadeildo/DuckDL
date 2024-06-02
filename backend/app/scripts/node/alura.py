import json

from app.scripts.base.node import Node
from app.scripts.base.utils import get_best_quality, get_soup, valid_tag


class AluraNode(Node):
    BASE_URL = "https://cursos.alura.com.br"

    async def _download(self):
        for child in self.children:
            await child.download()

        if self.type == "content":
            await self.__download_content()
        else:
            await self.log("node_success_downloaded")
            await self.node_service.set_status(self.id, "downloaded")

    async def _load_children(self):
        loaders = {
            "course": self.__load_modules,
            "module": self.__load_lessons,
            "lesson": self.__load_contents,
        }

        loader = loaders.get(self.type)
        if not loader:
            return

        await self.log("node_start_mapping_children")
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
                "order": i,
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

    async def __load_contents(self):
        soup = await get_soup(self.session.get, self.url)

        video_tag = valid_tag(soup.find("section", {"id": "video"}))
        if video_tag:
            await self.__get_video_content()

        await self.node_service.set_status(self.id, "mapped")
        await self.log(
            "node_success_mapped", children_type="content", count=len(self.children)
        )

    async def __get_video_content(self):
        video_qualities = (await self.session.get(f"{self.url}/video")).json()
        best_quality = get_best_quality(v["quality"] for v in video_qualities)
        for video in video_qualities:
            video_dump = {
                "name": f"Aula [{video['quality']}].mp4",
                "type": "content",
                "url": video["mp4"],
                "extra_infos": json.dumps(video),
                "should_download": video["quality"] == best_quality,
                **self.NODE_DEFAULTS,
            }

            node = AluraNode(**video_dump)
            await node.flush_node_db()
            self.children.append(node)

    async def __download_content(self):
        if self.path.exists():
            # TODO: check content size (bytes)
            await self.log("content_already_downloaded")
            return

        await self.log("node_start_download")
        await self.node_service.set_status(self.id, "downloading")
        with self.path.open("wb") as f:
            response = await self.session.get(self.url, stream=True)
            for chunk in response.iter_content(1024):
                f.write(chunk)

        await self.node_service.set_status(self.id, "downloaded")
        await self.log("node_success_downloaded")
