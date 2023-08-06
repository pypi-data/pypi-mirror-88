"""DOI tests."""
from typing import Any
from papersurfer.doi import Doi
from papersurfer.dtos import PaperDTO


def test_parse_doi_json(shared_datadir: Any) -> None:
    """Parse paper info."""
    datafiles = ['data_wo_author.json', 'doi-10.10292011jb008747.json',
                 'doi-wo-given-name.json', 'doi-wo-family-name.json']
    for datafile in datafiles:
        data = (shared_datadir / datafile).read_text(encoding='utf-8')
        doi = Doi()
        paper = doi.parse_doi_json(data)
        assert isinstance(paper, PaperDTO)
        assert paper.author
        assert paper.authors
        assert paper.title
        assert paper.journal
        assert paper.year
        assert paper.abstract
        assert paper.doi
        assert paper.slug
        if datafile == "data_wo_author.json":
            assert paper.slug == "N/A"


def test_get_info() -> None:
    """Return None for missing doi data."""
    Doi.load_doi_data = lambda _self, _doi: ""  # type: ignore
    info = Doi().get_info("dummy-doi")
    assert info is None
