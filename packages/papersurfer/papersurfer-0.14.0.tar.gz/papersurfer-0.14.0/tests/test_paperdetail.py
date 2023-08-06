"""Test parts of the ui."""
from papersurfer.ui.paperdetail import PaperDetail
from papersurfer.dtos import PostDTO


def details2text(details: PaperDetail) -> str:
    """Render details into string for testing."""
    return " ".join([e[0].text for e in details.render().contents])


def test_details() -> None:
    """Generate paper details popup."""
    details = PaperDetail()
    details.render()
    post = PostDTO(message="MSG", summary="summary")
    details.post = post
    assert details.post == post
#    details.paper = PaperDTO(title="Paper Title")
    text = details2text(details)
    assert "summary" in text
