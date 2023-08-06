"""Highlight string in strings."""
import re
import urwid  # type: ignore


def highlight(text: str, needle: str) -> urwid.Text:
    """Highlight a search term in a string."""
    text_items = []
    needle = needle or "ßß"
    needles = re.findall(needle, text, flags=re.IGNORECASE)
    hay = re.split(needle, text, flags=re.IGNORECASE)
    for i, item in enumerate(hay):
        text_items.append(('', item))
        if i < len(needles):
            text_items.append(('needle', needles[i]))

    return text_items
