from app.scripts.base.node import Node


class AluraNode(Node):
    async def download(self):
        print(
            "Isto daqui, é a função de download do aluraaaaaaa eeeeeee, ihul karalhooooo"
        )

    def load_children(self): ...
