"""Papersurfer main interface."""
import os
from typing import Any, Dict, List, Optional
from tinydb import TinyDB, Query
from .mattermost import Mattermost
from .bibtex import Bibtex
from .dtos import PostDTO, PaperDTO
from . import config


class Papersurfer:
    """Organize and cache paper/post data.

    This handles interaction with mattermost, doi and a local database.

    Papers and posts are similar but distinct concepts. A post contains
    information on a single mattermost entry, containing a paper reference.
    A paper contains information on a single scientific paper and a reference
    back to the mattermost post.
    """
    def __init__(self: "Papersurfer", url: str, channelname: str,
                 username: str, password: str) -> None:
        self.searchstring = ""

        self.mattermost = Mattermost(url, channelname, username, password)

        self.db_path = config.datadir

        self.db_posts: Any = None
        self.db_papers: Any = None
        self.db_files = {
            "posts": "papersurfer_posts_db.json",
            "papers": "papersurfer_papers_db.json",
        }
        self._posts: List[PostDTO] = []

    def load(self: "Papersurfer") -> None:
        """Load data from mattermost and save to storage."""
        self._connect_db()
        latest = self.get_latest_post()
        posts = self.mattermost.retrieve(latest["create_at"]
                                         if latest else None)
        self._update_db(posts=posts)

    def _connect_db(self: "Papersurfer") -> None:
        """Establish db connection. Noop if already connected."""
        if not self.db_posts:
            dbfile = os.path.join(self.db_path, self.db_files['posts'])
            self.db_posts = TinyDB(dbfile)  # type: ignore
        if not self.db_papers:
            dbfile = os.path.join(self.db_path, self.db_files['papers'])
            self.db_papers = TinyDB(dbfile)  # type: ignore

    def get_latest_post(self: "Papersurfer") -> Optional[Dict[str, Any]]:
        """Find the newest post and return."""
        posts = self.db_posts.all()
        if posts:
            posts.sort(reverse=True, key=lambda p: p["create_at"])

        return posts[0] if posts else None

    def _update_db(self: "Papersurfer", posts: Optional[List[PostDTO]] = None,
                   papers: Optional[List[PaperDTO]] = None) -> None:
        """Merge new data into database."""
        if posts:
            self._upsert_multiple(posts, self.db_posts)
        if papers:
            self._upsert_multiple(papers, self.db_papers)

    def _upsert_multiple(self: "Papersurfer", records: Any,
                         database: Any) -> None:
        """Update record in db unless it exits, then insert.

        Would be trivial if we could just change the unique id in tinydb to the
        doi property, but we can't.
        """
        for record in records:
            database.upsert(record.__dict__,
                            Query().doi == record.doi)  # type: ignore

    def _db_entry2post(self: "Papersurfer", entry: Dict[str, Any]) -> PostDTO:
        """Convert database entry to PostDTO."""
        return PostDTO(
            id=entry["id"],
            create_at=entry["create_at"],
            message=entry["message"],
            reporter=entry["reporter"],
            doi=entry["doi"],
            link=entry["link"] if "link" in entry else "",
            keywords=entry["keywords"] if "keywords" in entry else [],
            summary=entry["summary"] if "summary" in entry else "")

    def get_posts(self: "Papersurfer") -> List[PostDTO]:
        """Get all posts in storage."""
        if not self._posts:
            self._connect_db()
            self._posts = [self._db_entry2post(p) for p in self.db_posts.all()]
        return self._posts

    def filter_post(self: "Papersurfer", post: PostDTO,
                    searchstring: str) -> bool:
        """Determine if needle is in post."""
        searchstring = searchstring.lower()
        message = post.message.lower()
        reporter = post.reporter.lower()
        summary = post.summary.lower()
        keywords = (",".join(post.keywords)).lower()
        return (searchstring in message or searchstring in reporter
                or searchstring in summary or searchstring in keywords)

    def get_posts_filtered(self: "Papersurfer") -> List[PostDTO]:
        """Return a list of papers, filtered by filter."""
        return [post for post in self.get_posts()
                if self.filter_post(post, self.searchstring)]

    def get_papers(self: "Papersurfer") -> Any:
        """Get all papers in storage."""
        return self.db_papers.all()

    def export_to_bibtex(self: "Papersurfer") -> None:
        """Export current filtered list to bibtex file."""
        papers = self.get_posts_filtered()
        dois = [paper.doi for paper in papers]
        string = Bibtex().bib_from_dois(dois)
        with open("export.bib", 'w') as file:
            file.write(string)
