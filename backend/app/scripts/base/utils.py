from typing import Callable, Optional

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
