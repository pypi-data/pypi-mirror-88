"""Tests for mattermost adapter."""
import json
from typing import Any
from papersurfer.mattermost import Mattermost
from papersurfer.dtos import PostDTO


def test_get_posts_with_keywords_and_summaries(mocker: Any,
                                               shared_datadir: Any) -> None:
    """Check if posts can be loaded and parsed."""
    url = ""
    channelname = ""
    username = ""
    password = ""

    mattermost = Mattermost(url, channelname, username, password)

    with open((shared_datadir / "posts_keywords.json")) as fhandle:
        res = json.load(fhandle)

    mocker.patch('papersurfer.mattermost.Mattermost._get_reporter',
                 return_value="Name")
    mocker.patch('papersurfer.mattermost.Mattermost.login',
                 return_value=True)
    mocker.patch('papersurfer.mattermost.Mattermost._get_posts_for_channel',
                 return_value=res)

    posts = mattermost.retrieve()

    assert len(posts) == 3
    assert isinstance(posts[2], PostDTO)

    assert "Probabilistic hazard maps for operational use" in posts[1].message
    assert "Holuhraun" in posts[1].keywords
    assert "The Holuhraun fissure eruption" in posts[1].summary

    assert "Mantle and crustal sources" in posts[2].message
    assert not posts[2].keywords
    assert "We present a new high‐resolution seismic model" in posts[2].summary

    assert "Automatic detection of volcanic surface" in posts[0].message
    assert not posts[0].keywords
    assert "Novel application of CNN is capable" in posts[0].summary
