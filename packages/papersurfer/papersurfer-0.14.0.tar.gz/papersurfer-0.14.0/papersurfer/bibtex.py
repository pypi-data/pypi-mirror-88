"""Simplified DOI interface."""
from typing import List
from .doi import Doi


class Bibtex:
    """Interface for bibtex string."""
    def entry_from_doi(self: 'Bibtex', doi: str) -> str:
        """Get bibtex string for doi."""
        return Doi().get_bibtex(doi)

    def bib_from_dois(self: 'Bibtex', dois: List[str]) -> str:
        """Get bibtex string for mulitple dois."""
        return "\n".join([Doi().get_bibtex(doi) for doi in dois])
