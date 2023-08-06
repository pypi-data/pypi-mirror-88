"""Simplified DOI interface."""
import json
import re
import string
import logging
from typing import Optional, Dict
import requests
from .dtos import PaperDTO
from . import config


class Doi:
    """Interface w/ the doi.org api."""

    _cache: Dict[str, PaperDTO] = {}

    def get_doi_link(self: 'Doi', doi: str) -> str:
        """Assemble doi link."""
        return f"http://doi.org/{doi}"

    def load_doi_data(self: 'Doi', doi: str) -> str:
        """Load data for doi."""
        headers = {
            'Accept': 'application/json',
        }
        return requests.get(f'http://dx.doi.org/{doi}',
                            headers=headers).text

    def parse_doi_json(self: 'Doi', jsoncontent: str) -> PaperDTO:
        """Tranform doi json to PaperDTO."""
        info = json.loads(jsoncontent)

        if config.debug:
            filename = format_filename(f"doi-{info['DOI']}.json")
            with open(filename, "w") as file:
                json.dump(info, file, indent=4)

            if 'author' in info and info['author'][0]['sequence'] != 'first':
                logging.error("incorrect first author %s", jsoncontent)

        author = (f"{info['author'][0]['given']} {info['author'][0]['family']}"
                  if "author" in info
                  else "Author N/A")

        authors = (", ".join([(f"{a['given'] if 'given' in a else ''} "
                               f"{a['family'] if 'family' in a else ''} "
                               f"{a['name'] if 'name' in a else ''}").strip()
                              for a in info['author']])
                   if "author" in info
                   else "Authors N/A")

        title = (info['title']
                 if "title" in info and isinstance(info['title'], str)
                 else "Title N/A")
        journal = (info['publisher']
                   if "publisher" in info
                   else "Journal N/A")
        year = info['created']['date-parts'][0][0]
        doi = info['DOI']
        abstract = info['abstract'] if "abstract" in info else "Abstract N/A"

        slug = (f"{info['author'][0]['family']}{year}"
                if "author" in info else "N/A")

        return PaperDTO(author, authors, title, journal, year, abstract, doi,
                        slug)

    def get_bibtex(self: 'Doi', doi: str) -> str:
        """Get bibtex string for doi.

        Try also:
        curl -LH "Accept: text/bibliography; style=bibtex" \
                    http://dx.doi.org/10.1007/s00445-020-01390-8

        """
        headers = {
            'Accept': 'text/bibliography; style=bibtex',
        }
        req = requests.get(f'http://dx.doi.org/{doi}', headers=headers)

        # guess and set correct encoding
        req.encoding = "utf-8"

        return req.text

    def get_info(self: 'Doi', doi: str) -> Optional[PaperDTO]:
        """Get information for doi."""
        if doi in self._cache:
            return self._cache[doi]
        try:
            jsoncontent = self.load_doi_data(doi)
            data = self.parse_doi_json(jsoncontent)
            self._cache[doi] = data
            return data
        except json.decoder.JSONDecodeError:
            if config.debug:
                with open(format_filename(doi+"-broken.txt"), "w") as file:
                    file.write(str(jsoncontent))

            return None

    def extract_doi(self: 'Doi', hay: str) -> Optional[str]:
        """Parse doi from string, or None if not found.

        >>> Doi().extract_doi("https://doi.org/10.1093/petrology/egaa077")
        '10.1093/petrology/egaa077'
        """
        pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        matches = re.compile(pattern, re.I).search(hay)
        return matches.group() if matches else None


def format_filename(inputstr: str) -> str:
    """Take a string and return a valid filename constructed from the string.

    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    https://gist.github.com/seanh/93666
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in inputstr if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename
