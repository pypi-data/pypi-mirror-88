"""Bibtex tests."""
from typing import Any
import pytest
from papersurfer.bibtex import Bibtex


@pytest.mark.skip(reason="needs network")  # type: ignore
def test_entry_from_doi(shared_datadir: Any) -> None:
    """Load bibtex data for doi."""
    dois = ["10.1016/j.chemgeo.2020.119702", "10.1029/2019jb019149"]

    for doi in dois:
        # FIXME: request needs to be mocked pylint # pylint: disable=fixme
        #  requests_mock.get(f"", text="")
        entry = Bibtex().entry_from_doi(doi)

        filename = doi.replace("/", "__") + ".bibtex"
        with open(shared_datadir / filename, "r") as file:
            assert entry == file.read()
