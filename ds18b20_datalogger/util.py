import itertools
from typing import Any, Generator, List


def partition(lst, chunksize: int) -> Generator[List[Any], None, None]:
    """
    Partition a list into equal sized chunks.

    Split a List into Chunks of Given Size in Python
    https://favtutor.com/blogs/partition-list-python
    """
    for i in range(0, len(lst), chunksize):
        yield list(itertools.islice(lst, i, i + chunksize))


def msg(text: str):
    """
    Return a text armoured with ANSI codes to make it appear in bright yellow.
    """
    return f"\033[1;33m{text}\033[0m"
