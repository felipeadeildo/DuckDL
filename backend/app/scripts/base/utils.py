import re
from typing import Callable, Iterable, Optional

from app.scripts.base.constants import POSSIBLE_QUALITIES, QUALITIES_PRIORITY
from bs4 import BeautifulSoup, NavigableString, Tag


async def get_soup(method: Callable, url: str, debug: bool = False, *args, **kwargs):
    """Get BeautifulSoup object from given url with given method (async)

    Args:
        method (Callable): requests method
        url (str): url

    Keyword Args:
        *args: arguments
        **kwargs: keyword arguments

    Returns:
        BeautifulSoup: BeautifulSoup object
    """
    res = await method(url, *args, **kwargs)
    if debug:
        with open("debug.html", "wb") as f:
            f.write(res.content)
    return BeautifulSoup(res.content, "html.parser")


def valid_tag(tag: Optional[Tag | NavigableString]) -> Optional[Tag]:
    """Get the real tag (to avoid Nones and NavigableStrings that lint complains)

    Args:
        tag (Optional[Tag  |  NavigableString]): The tag

    Returns:
        Optional[Tag]: The real tag if it's not None or NavigableString
    """
    if isinstance(tag, NavigableString) or tag is None:
        return None
    return tag


def get_node_default_params(instance: object) -> dict:
    """Get the default params for the given node

    Args:
        instance (Union[Node, PlatformDownloader]): The node

    Returns:
        dict: The default params
    """
    return {
        "prisma": getattr(instance, "prisma"),
        "account": getattr(instance, "account"),
        "settings": getattr(instance, "settings"),
        "session": getattr(instance, "session"),
    }


def get_best_quality(qualities: Iterable[POSSIBLE_QUALITIES]) -> POSSIBLE_QUALITIES:
    """Get the best quality from the given qualities

    Args:
        qualities (Iterable[POSSIBLE_QUALITIES]): The qualities

    Returns:
        str: The best quality
    """
    return min(qualities, key=lambda q: QUALITIES_PRIORITY[q])


def sanitize_name(name: str) -> str:
    """Make the name folder friendly
    - remove special characters to create folder/file names safely

    Args:
        name (str): The name

    Returns:
        str: The sanitized name
    """
    return re.sub(r"[?<>/:;*&$#@!\"'{}\\+=^]", "_", name).strip()
