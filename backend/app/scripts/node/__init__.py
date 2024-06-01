from typing import Mapping

from app.scripts.base.node import Node
from app.scripts.node.alura import AluraNode

nodes: Mapping[str, type[Node]] = {
    "alura": AluraNode,
}
