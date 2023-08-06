"""Simplified mattermost interface."""
import logging
import time
import json
import re
from typing import Optional, List, Dict, Any
import requests
import mattermostdriver  # type: ignore
from .exceptions import ConfigError
from .dtos import PostDTO
from .doi import Doi
from . import config


def extract_by_keyword(keyword: str, text: str, indicators: List[str]) -> str:
    """Extract content by keyword.

    >>> text = "Keywords: keyword1, keyword2"
    >>> extract_by_keyword("Keywords:", text, ["Keyword"])
    ' keyword1, keyword2'
    >>> text = "Keywords: keyword1, keyword2"
    >>> extract_by_keyword("Keywords:", text, [])
    ' keyword1, keyword2'
    """
    pattern = '{}(.*)((?:\n.*?)+?)?({}|$)'
    try:
        expression = pattern.format(keyword, "|".join(indicators))
        matches = re.findall(expression, text, flags=re.IGNORECASE)
        return "".join(matches[0][0:-1])
    except IndexError:
        return ""


def extract_summary_keywords(text: str) -> Dict[str, Any]:
    r"""Parse keywords and summary from post messages.

    >>> text = "Keywords: keyword1, keyword2"
    >>> extract_summary_keywords(text)
    {'keywords': ['keyword1', 'keyword2'], 'summary': '', 'message': ''}

    >>> text = "Keywords: keyword1; keyword2"
    >>> extract_summary_keywords(text)
    {'keywords': ['keyword1', 'keyword2'], 'summary': '', 'message': ''}

    >>> text = "Keywords: \n keyword1 \n keyword2"
    >>> extract_summary_keywords(text)
    {'keywords': ['keyword1', 'keyword2'], 'summary': '', 'message': ''}

    >>> text = "Summary: Test summary"
    >>> extract_summary_keywords(text)
    {'keywords': [], 'summary': 'Test summary', 'message': ''}

    >>> text = "Key points: Test key points"
    >>> extract_summary_keywords(text)
    {'keywords': [], 'summary': 'Test key points', 'message': ''}

    >>> text = '''Some Paper
    ... DOI: 1234.12/12
    ...
    ... keywords: Stu**[a-n]ff, Interest$
    ...
    ... summary:
    ... Interesting stuff
    ... more'''
    >>> r = extract_summary_keywords(text)  # doctest: +ELLIPSIS
    >>> r['keywords']
    ['Stu**[a-n]ff', 'Interest$']
    >>> r['summary']
    'Interesting stuff\nmore'
    >>> r['message']
    'Some Paper\nDOI: 1234.12/12'

    >>> text = '''Some Paper
    ... Key Points
    ... Interesting stuff'''
    >>> extract_summary_keywords(text)
    {'keywords': [], 'summary': 'Interesting stuff', 'message': 'Some Paper'}

    # TODO:
    # >>> text = '''Storage and Evolution
    # ... Jacob D. Klug [Klug2020]
    # ... https://doi.org/10.1029/2020JB019475
    # ...     Magma storage
    # ...     Mafic recharge
    # ... '''
    # >>> r = extract_summary_keywords(text)
    # >>> r['message']
    # ''
    """
    # some phrases that indicate a summary or keyword section
    summaryindicator = ["key points:", "key points\n", "keypoints:",
                        "keypoints\n", "summary:", "summary\n"]
    keywordindicator = ["keywords:"]
    indicators = summaryindicator + keywordindicator

    kwstrs = ""
    for keyword in keywordindicator:
        kwstr = extract_by_keyword(keyword, text, indicators)
        textsearch = re.compile(re.escape(keyword + kwstr), re.IGNORECASE)
        text = textsearch.sub('', text)
        kwstrs += kwstr

    keywords = [kw.strip() for kw in re.split(',|;|\n', kwstrs.strip()) if kw]

    summary = ""
    for keyword in summaryindicator:
        kwstr = extract_by_keyword(keyword, text, indicators)
        textsearch = re.compile(keyword + kwstr, re.IGNORECASE)
        text = textsearch.sub('', text)
        summary += kwstr

    return {"keywords": keywords,
            "summary": summary.strip(),
            "message": text.strip()}


class Mattermost:
    """Provide a simplified interaction w/ mattermost api."""
    def __init__(self: 'Mattermost', url: str, channelname: str, username: str,
                 password: str) -> None:
        self.posts: List[PostDTO] = []
        self._mattermost = mattermostdriver.Driver({
            'url': url,
            'login_id': username,
            'password': password,
            'port': 443
        })

        self.teamname = ""
        self._url = url
        self._loggedin = False
        self._reporters: Dict[str, str] = {}
        self._channelname = channelname
        self._channel: Optional[str] = None

    def login(self: 'Mattermost') -> None:
        """Log into mattermost and raise ConfigError on fail."""
        try:
            self._mattermost.login()
        except requests.exceptions.ConnectionError:
            print("Mattermost url is incorrect.")
            raise ConfigError from requests.exceptions.ConnectionError
        except (mattermostdriver.exceptions.NoAccessTokenProvided,
                requests.exceptions.InvalidURL,
                requests.exceptions.HTTPError) as exception:
            print("Failed to log into Mattermost.")
            raise ConfigError from exception

        try:
            self._channel = self._get_channel(self._channelname)
        except ConfigError:
            print("Couldn't find Mattermost channel.")
            raise ConfigError from ConfigError

        self._loggedin = True

    def _get_channel(self: "Mattermost", channelname: str) -> Any:
        """Try to find the paper channel by display name."""
        teamapi = self._mattermost.teams
        channelapi = self._mattermost.channels

        for team in teamapi.get_user_teams("me"):
            channels = [channel["id"] for channel
                        in channelapi.get_channels_for_user("me", team["id"])
                        if channel["display_name"] == channelname]
            if channels:
                # lets just hope no-one has the same channel name in multiple
                # teams
                self.teamname = team["name"]
                return channels[0]

        print(f"Channel {channelname} does not exits")
        raise ConfigError

    def _get_reporter(self: "Mattermost", userid: str) -> str:
        """Load user from mattermost api and cache."""
        userapi = self._mattermost.users
        if userid not in self._reporters:
            self._reporters[userid] = userapi.get_user(userid)["username"]

        return self._reporters[userid]

    def _get_posts_for_channel(self: "Mattermost",
                               since: Optional[int]) -> List[Dict[str, Any]]:
        """Get posts from mattermost and concat paged response since date."""
        params = {"since": since} if since else {}
        posts = []

        while True:
            resp = self._mattermost.posts.get_posts_for_channel(
                self._channel, params)
            posts.extend(resp['posts'].values())
            if resp["prev_post_id"]:
                params["before"] = resp["prev_post_id"]
            else:
                break

        return posts

    def _retrieve_all_posts(self: "Mattermost",
                            since: Optional[int]) -> List[PostDTO]:
        """Retrieve all posts from mattermost, unfiltered for papers."""
        start = time.perf_counter()
        posts = self._get_posts_for_channel(since)
        dtos: List[PostDTO] = []

        # follow children for each paper post and
        # try to extract meta information
        if config.debug:
            with open("all_posts.json", "w") as filehandle:
                json.dump(posts, filehandle, indent=4)

        for post in posts:
            doi = Doi().extract_doi(post['message'])
            if doi is not None:
                dtos.append(PostDTO(
                            id=post['id'],
                            create_at=post['create_at'],
                            message=post['message'],
                            reporter=self._get_reporter(post['user_id']),
                            link=(f"https://{self._url}/"
                                  f"{self.teamname}/pl/{post['id']}"),
                            doi=doi,))

        for dto in dtos:
            res = extract_summary_keywords(dto.message)
            dto.message = res['message']
            dto.summary += res['summary']
            dto.keywords.extend(res['keywords'])

            children = [p["message"] for p in posts if p["root_id"] == dto.id]
            for child in children:
                res = extract_summary_keywords(child)
                dto.summary += res['summary']
                dto.keywords.extend(res['keywords'])

        logging.debug("retrieving and processing %i mattermost posts took %f",
                      len(posts), time.perf_counter() - start)

        return dtos

    # def is_paperpost(self: "Mattermost", post: Dict[str, Any]) -> bool:
    #     """Check if post contains a paper reference."""
    #     return Doi().extract_doi(post['message']) is not None

    def retrieve(self: "Mattermost",
                 since: Optional[int] = None) -> List[PostDTO]:
        """Retrieve papers from mattermost channel."""
        if not self._loggedin:
            self.login()
        self.posts = self._retrieve_all_posts(since)
        return self.posts

    def check_doi_exits(self: "Mattermost", doi: str) -> bool:
        """Check for doi in current paper list."""
        doi_needle = Doi().extract_doi(doi)
        posts_found = [post for post in self.posts if post.doi == doi_needle]
        return bool(posts_found)

    def post(self: "Mattermost", message: str) -> None:
        """Post message to thread."""
        self._mattermost.posts.create_post({"channel_id": self._channel,
                                            "message": message})
