"""Improved Button."""
from typing import Any, Callable, Dict, Optional
import urwid  # type: ignore


class PrettyButton(urwid.WidgetWrap):  # type: ignore
    """Prettified urwid Button."""
    def __init__(self: "PrettyButton", label: str,
                 on_press: Optional[Callable[[Any], Any]] = None,
                 user_data: Optional[Dict[str, Any]] = None) -> None:
        self.label = ""
        self.text = urwid.Text("")
        self.set_label(label)
        self.widget = urwid.AttrMap(self.text, '', 'highlight')

        # use a hidden button for evt handling
        self._hidden_btn = urwid.Button(f"hidden {self.label}",
                                        on_press, user_data)

        super().__init__(self.widget)

    def selectable(self: "PrettyButton") -> bool:
        """Make button selectable."""
        return True

    def keypress(self: "PrettyButton", *args: Any, **kw: Any) -> Any:
        """Handle keypresses."""
        return self._hidden_btn.keypress(*args, **kw)

    def mouse_event(self: "PrettyButton", *args: Any, **kw: Any) -> Any:
        """Handle mouse events."""
        return self._hidden_btn.mouse_event(*args, **kw)

    def get_label(self: "PrettyButton") -> str:
        """Return current input label."""
        return self.label

    def set_label(self: "PrettyButton", label: str) -> None:
        """Return current input label."""
        self.label = label
        self.text.set_text(f"[ {label} ]")
