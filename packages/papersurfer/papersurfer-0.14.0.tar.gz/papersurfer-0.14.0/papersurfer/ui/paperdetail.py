"""Element to display paper details."""
from typing import Dict
import urwid  # type: ignore
from ..dtos import PaperDTO, PostDTO
from .highlight import highlight


class PaperDetail:
    """Render details to a post, including async paper data."""
    def __init__(self: "PaperDetail") -> None:
        self._papers: Dict[str, PaperDTO] = {}
        self._post = PostDTO()
        self._paper = PaperDTO()

        self.keywords = urwid.Text("")
        self.summary = urwid.Text("")
        self.paper_title = urwid.Text("")
        self.paper_authors = urwid.Text("")
        self.paper_journal = urwid.Text("")
        self.paper_doi = urwid.Text("")
        self.paper_abstract = urwid.Text("")
        self.bibtex = urwid.Text("")

#        self.updatecounter = 0
#        self.updates = urwid.Text("")

        self._searchstring = ""

    @property
    def post(self: "PaperDetail") -> PostDTO:
        """Get post."""
        return self._post

    @post.setter
    def post(self: "PaperDetail", post: PostDTO) -> None:
        """Set post, reload paper, re-render."""
        self._post = post
        self._paper = (self._papers[post.doi]
                       if post.doi in self._papers
                       else PaperDTO())
        self._update()

    @property
    def papers(self: "PaperDetail") -> Dict[str, PaperDTO]:
        """Get papers."""
        return self._papers

    @papers.setter
    def papers(self: "PaperDetail", papers: Dict[str, PaperDTO]) -> None:
        """Set papers and re-render if applicable."""
        self._papers = papers
        self._paper = (self._papers[self._post.doi]
                       if self._post.doi in self._papers
                       else PaperDTO())
        self._update()

    @property
    def searchstring(self: "PaperDetail") -> str:
        """Get searchstring."""
        return self._searchstring

    @searchstring.setter
    def searchstring(self: "PaperDetail", searchstring: str) -> None:
        """Set searchstring and update."""
        self._searchstring = searchstring
        self._update()

    def _update(self: "PaperDetail") -> None:
        """Re-render content."""
        self.summary.set_text(highlight(self._post.summary, self.searchstring))
        self.keywords.set_text(
            highlight(", ".join(self._post.keywords), self.searchstring))
        self.paper_title.set_text(
            highlight(self._paper.title, self.searchstring))
        self.paper_authors.set_text(
            highlight(self._paper.authors, self.searchstring))
        self.paper_journal.set_text(
            highlight(self._paper.journal, self.searchstring))
        self.paper_doi.set_text(highlight(self._paper.doi, self.searchstring))
        self.paper_abstract.set_text(
            highlight(self._paper.abstract, self.searchstring))
#        self.updatecounter += 1
#        self.updates.set_text("Updates: " + str(self.updatecounter))

    def render(self: "PaperDetail") -> urwid.Pile:
        """Create Dialog with paper details."""
        body_pile = urwid.Pile([
            self.paper_title,
            self.paper_authors,
            self.paper_journal,
            self.paper_doi,
            self.paper_abstract,
            self.summary,
            self.bibtex,
            self.keywords,
            # self.updates
        ])

        return body_pile
