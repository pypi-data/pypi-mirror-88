"""Dialog to add another post to public list."""
from typing import Any, Callable
import urwid  # type: ignore
from papersurfer.mattermost import Mattermost
from .prettybutton import PrettyButton
from ..doi import Doi
from ..dtos import PaperDTO


class PostDialog(urwid.WidgetWrap):  # type: ignore
    """Dialog to submit a new paper to mattermost thread.

    UI:
        DOI: [ _________________]
        Generated Message:
            "# # # #  # # # #"

        [Submit]       [Close]
    """
    def __init__(self: "PostDialog", mattermost: Mattermost,
                 close: Callable[[Any], Any], loop: Any) -> None:
        self._loop = loop
        self.alarm_handle = None

        self.doi: str = ""
        self.msg: str = ""
        self.mattermost = mattermost
        self.close = close
        self.doi_input = urwid.Edit("Doi: ")
        urwid.connect_signal(self.doi_input, 'change', self.h_input)
        self.doi_result = urwid.Text("")

        body_pile = urwid.Pile([
            self.doi_input,
            urwid.Divider(" "),
            self.doi_result,
            urwid.Divider(" "),
            urwid.Columns([
                PrettyButton("Close", self.close),
                PrettyButton("Submit", self.submit)
            ]),
        ])
        body_filler = urwid.Filler(body_pile, valign='top')
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)
        frame = urwid.Frame(body,
                            header=urwid.Text("Submit new paper to list"))

        self.widget = frame

        super().__init__(self.widget)

    def submit(self: "PostDialog", _: Any) -> None:
        """Submit post to thread."""
        if not self.mattermost.check_doi_exits(self.doi):
            self.mattermost.post(self.msg)
        self.close(_)

    def create_mgs(self: "PostDialog", paper: PaperDTO) -> str:
        """Format post message."""
        msg = f"""\
{paper.title}
{paper.authors}
{paper.journal} [{paper.slug}]
{Doi().get_doi_link(paper.doi)}"""
        return msg

    def h_input(self: "PostDialog", _: Any, doi: str) -> None:
        """Handle doi input field and debounce."""
        self.doi_result.set_text("")
        self.doi = ""
        self.msg = ""

        self._loop.remove_alarm(self.alarm_handle)
        self.alarm_handle = self._loop.set_alarm_in(.5, self.search_doi, doi)

    def search_doi(self: "PostDialog", _loop: Any, doi: str) -> None:
        """Trigger search for paper ref by doi and update ui."""
        self.doi_result.set_text("... loading ...")
        self._loop.draw_screen()
        if Doi().extract_doi(doi):
            paper = Doi().get_info(doi)
            if paper:
                if self.mattermost.check_doi_exits(doi):
                    self.doi_result.set_text(f"{self.create_mgs(paper)} \n"
                                             "-> Paper already posted! <-")
                else:
                    self.doi_result.set_text(self.create_mgs(paper))
                    self.doi = doi
                    self.msg = self.create_mgs(paper)
            else:
                self.doi_result.set_text("Doi not found.")
            return

        self.doi_result.set_text("invalid doi")
