"""Text user interface main."""
from functools import partial
import sys
import logging
import asyncio
import webbrowser
from typing import Any, Dict
import urwid  # type: ignore
from ..papersurfer import Papersurfer
from ..exceptions import ConfigError
from ..doi import Doi
from ..dtos import PostDTO, PaperDTO
from .postdialog import PostDialog
from .prettybutton import PrettyButton
from .paperdetail import PaperDetail
from .highlight import highlight


class PapersurferUi:
    """Provide UI and interface with mattermost class."""

    _palette = [
        ('button', 'default,bold', 'default'),
        ('I say', 'default,bold', 'default', 'bold'),
        ('needle', 'default, bold, underline', 'default', 'bold'),
        ('highlight', 'black', 'dark blue'),
        ('banner', 'black', 'light gray'),
        ('selectable', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('papertitle', 'default,bold', 'default', 'bold')
    ]

    def __init__(self: "PapersurferUi", url: str, channel: str, username: str,
                 password: str) -> None:
        self.papersurfer = Papersurfer(url, channel, username, password)

        # TODO: move to Papersurfer or cache DOI.getInfo
        self.papers: Dict[str, PaperDTO] = {}
        self._screen = urwid.raw_display.Screen()

        self.size = self._screen.get_cols_rows()

        ask = urwid.Edit(('I say', u"Filter?\n"))
        exitbutton = PrettyButton(u'Exit', on_press=self.on_exit_clicked)
        self.exportbutton = PrettyButton(u'Export filtered list as bibtex',
                                         on_press=self.on_export_clicked)
        submitbutton = PrettyButton('Submit paper',
                                    on_press=self.open_submit_paper)
        div = urwid.Divider(u'-')

        body = [urwid.Text("")]
        self.listcontent = urwid.SimpleFocusListWalker(body)
        self.post_list = urwid.ListBox(self.listcontent)
        paperlist = urwid.BoxAdapter(self.post_list, self.size[1] - 5)

        urwid.connect_signal(self.listcontent, "modified", self._h_list_focus)

        buttonrow = urwid.Columns([exitbutton, self.exportbutton,
                                   submitbutton])
        self.paperdetail = PaperDetail()
        self.pile = urwid.Pile([ask,
                                div,
                                # TODO: horizontal or vertical
                                urwid.Columns([paperlist,
                                               self.paperdetail.render()]),

                                div,
                                buttonrow])
        self.top = urwid.Filler(self.pile, valign='middle')
        self._over = urwid.Overlay(
            self.loading_indicator(),
            self.top,
            align='center',
            valign='middle',
            width=20,
            height=10
        )

        urwid.connect_signal(ask, 'change', self.onchange)

        self.loop = asyncio.get_event_loop()
        evl = urwid.AsyncioEventLoop(loop=self.loop)
        self.mainloop = urwid.MainLoop(self._over, self._palette,
                                       unhandled_input=self._h_unhandled_input,
                                       event_loop=evl)

        self.loop.run_in_executor(None, self._load_list)
        self.loop.run_in_executor(None, self._update_data)

        self.mainloop.run()
        try:
            self.papersurfer.mattermost.login()
        except ConfigError:
            sys.exit(1)

    def _h_list_focus(self: "PapersurferUi") -> None:
        post_idx = self.post_list.get_focus()[1]
        if post_idx is not None:
            post = self.papersurfer.get_posts_filtered()[post_idx]
            self.loop.run_in_executor(None, self._load_doi, post.doi)
        else:
            post = PostDTO()
        self.paperdetail.post = post

    def _load_doi(self: "PapersurferUi", doi: str) -> None:
        if doi not in self.papers:
            self.papers[doi] = Doi().get_info(doi) or PaperDTO()

        # kick paperdetail to let it know new data is available
        self.paperdetail.papers = self.papers

    def _h_unhandled_input(self: "PapersurferUi", key: str) -> None:
        """Handle keyboard input not otherwise handled."""
        if key == "esc":
            raise urwid.ExitMainLoop()

    def _h_load_list(self: "PapersurferUi", _loop: Any, _data: Any) -> None:
        """Handle load list alarm."""
        self._load_list()

    def _load_list(self: "PapersurferUi") -> None:
        """Load and display paper list."""
        posts = self.papersurfer.get_posts()
        if posts:
            body = [self.list_item(post) for post in posts]
            self.listcontent.clear()
            self.listcontent.extend(body)
            self.mainloop.widget = self.top

    def _h_update_data(self: "PapersurferUi", _loop: Any, _data: Any) -> None:
        """Handle update data alarm."""
        self._update_data()

    def _update_data(self: "PapersurferUi") -> None:
        """Load and display paper list."""
        try:
            self.papersurfer.load()
        except ConfigError:
            logging.error("Failed to retrieve data from mattermost.")
            raise urwid.ExitMainLoop() from ConfigError
        self._load_list()

    def loading_indicator(self: "PapersurferUi") -> Any:
        """Create loading indicator dialog."""
        body_text = urwid.Text("Loading...", align='center')
        body_filler = urwid.Filler(body_text, valign='middle')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )

        return urwid.Frame(body_padding)

    def list_item(self: "PapersurferUi", post: PostDTO,
                  needle: str = "") -> Any:
        """Render a post in the list of posts."""
        text = f"{post.message} ({post.reporter})"
        title = urwid.Text(highlight(text, needle))

        discuss_button = PrettyButton("Open Discussion",
                                      on_press=partial(self.h_open_discussion,
                                                       post))
        doi_button = PrettyButton("Open DOI",
                                  on_press=partial(self.h_open_doi, post))

        button_bar = urwid.Columns([discuss_button, doi_button])
        pile = urwid.Pile([title, button_bar, urwid.Divider()])
        return pile

    def updscrn(self: "PapersurferUi") -> None:
        """Update (redraw) screen."""
        self.mainloop.draw_screen()

    def onchange(self: "PapersurferUi", _: Any, needle: str) -> None:
        """Handle filter change."""
        self.papersurfer.searchstring = needle
        self.paperdetail.searchstring = needle
        self.listcontent.clear()
        self.listcontent.extend([
            self.list_item(paper, needle)
            for paper in self.papersurfer.get_posts_filtered()])

    def running_export(self: "PapersurferUi", state: bool) -> None:
        """Set exporting state."""
        label = self.exportbutton.get_label()
        running_indicator = " (running...)"
        if state:
            self.exportbutton.set_label(label + running_indicator)
        else:
            self.exportbutton.set_label(label.replace(running_indicator, ""))
        self.updscrn()

    def on_exit_clicked(self: "PapersurferUi", _: Any) -> None:
        """Handle exitbutton click and exit."""
        raise urwid.ExitMainLoop()

    def on_export_clicked(self: "PapersurferUi", _: Any) -> None:
        """Handle exitbutton click and exit."""
        self.running_export(True)
        self.papersurfer.export_to_bibtex()
        self.running_export(False)

    def h_open_discussion(self: "PapersurferUi", post: PostDTO,
                          _: Any) -> None:
        """Handle click/enter on discussion button."""
        self.open_discussion(post)

    def h_open_doi(self: "PapersurferUi", post: PostDTO, _: Any) -> None:
        """Handle click/enter on doi button."""
        self.open_doi(post)

    def open_discussion(self: "PapersurferUi", post: PostDTO) -> None:
        """Open Mattermost post in browser."""
        webbrowser.open(post.link)

    def open_doi(self: "PapersurferUi", post: PostDTO) -> None:
        """Open paper page in browser."""
        webbrowser.open(Doi().get_doi_link(post.doi))

    def h_close_dialog(self: "PapersurferUi", _: Any) -> None:
        """Handle close dialog button."""
        self.close_dialog()

    def close_dialog(self: "PapersurferUi") -> None:
        """Close currently open dialog."""
        self.mainloop.widget = self.top

    def h_close_submit_paper(self: "PapersurferUi", _: Any) -> None:
        """Reload fresh data when closing submit paper dialog."""
        self._update_data()
        self.close_dialog()

    def open_submit_paper(self: "PapersurferUi", _: Any) -> None:
        """Open submit paper dialog."""
        self._over = urwid.Overlay(
            PostDialog(self.papersurfer.mattermost,
                       self.h_close_submit_paper, self.mainloop),
            self.top,
            align='center',
            valign='middle',
            width=100,
            height=200
        )

        self.mainloop.widget = self._over
