"""Data transfer objects."""
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass, field
from typing import List


@dataclass
class PostDTO:
    """Encapsulate Mattermost Posts."""
    id: str = ""
    link: str = ""
    create_at: int = -1
    message: str = ""
    reporter: str = ""
    doi: str = ""
    keywords: List[str] = field(default_factory=list)
    summary: str = ""

    def __str__(self: "PostDTO") -> str:
        return self.message + '\n' + str(self.keywords) + '\n' + self.summary


@dataclass
class PaperDTO:
    """Encapsulate Paper meta data."""
    author: str = ""
    authors: str = ""
    title: str = ""
    journal: str = ""
    year: int = 0
    abstract: str = ""
    doi: str = ""
    slug: str = ""
