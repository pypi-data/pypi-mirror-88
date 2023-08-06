"""Paper surfer - browse papers posted on the mattermost channel.

UI:

[____(filter)______]
1. paper (open discussion) (open paper)
2. paper (open discussion) (open paper)
3. paper (open discussion) (open paper)
4. paper (open discussion) (open paper)

"""
import time
import os
import sys
import logging
import pathlib
from typing import Any, List
import configargparse  # type: ignore
from xdgappdirs import AppDirs  # type: ignore
from .exceptions import ConfigError
from .mattermost import Mattermost
from .bibtex import Bibtex
from . import config
from .papersurfer import Papersurfer
from .ui.papersurferui import PapersurferUi


def get_config_file_paths() -> List[str]:
    """Find config file paths.

    The first config file that is found is used, it is searched for (in
    this order), at:
     - config, if set (e.g. from the cli)
     - from the default source path (./papersurfer.conf)
     - home config path (system-dependent,
        see https://pypi.org/project/xdgappdirs/ for details)
     - system path (system-dependent,
        see https://pypi.org/project/xdgappdirs/ for details)

    >>> type(get_config_file_paths())
    <class 'list'>
    """
    appdir = AppDirs("papersurfer")
    paths = [appdir.site_config_dir, appdir.user_config_dir, "./"]
    default_filename = "papersurfer.conf"

    return [os.path.join(p, default_filename) for p in paths]


def get_log_file_path() -> str:
    """Get log file path."""
    path = AppDirs("papersurfer").user_log_dir
    default_filename = "papersurfer.log"

    return os.path.join(path, default_filename)


def interactive_configuration() -> Any:
    """Query user for credentials."""
    url = input("Mattermost URL (eg. mattermost.example.net): ")
    url = url.replace("https://", "").strip('/')  # cleanup https://mtm/ urls
    channel = input("Channel (eg. Paper Club): ")
    username = input("Username (same as mattermost login, "
                     "eg. JohnDoe@example.net): ")
    password = input("Password (same as mattermost login, eg. SuperSecret1): ")
    return url, channel, username, password


def get_version() -> str:
    """Get version number from static version text file."""
    pkgbase = pathlib.Path(__file__).parent
    with open(f"{pkgbase}/_version.txt", "r") as versionfile:
        return versionfile.read()


def print_paths() -> None:
    """Get paths of config, log and data files."""
    paths = get_config_file_paths()
    paths.append(get_log_file_path())
    paths.append(config.datadir)
    paths = [p for p in paths if os.path.exists(p)]
    print("\n".join(paths))


def parse_args() -> Any:
    """Parse command line arguments and config file."""
    parser = configargparse.ArgParser(
        default_config_files=get_config_file_paths())
    parser.add("-w", "--write-out-config-file",
               help="takes the current command line args and writes them out "
                    "to a config file at the given path",
               is_write_out_config_file_arg=True)
    parser.add('-c', '--config', required=False, is_config_file=True,
               help='config file path')
    parser.add('--url', required=False, help='Mattermost url')
    parser.add('--channel', required=False, help='Mattermost channel')
    parser.add('-u', '--username', required=False, help='Mattermost username')
    parser.add('-p', '--password', required=False, help='Mattermost password')
    parser.add('--dump-posts', action='store_true',
               help="Dump mattermost paper posts to stdout and exit")
    parser.add('--dump-bibtex', action='store_true',
               help="Dump bibtex collection to stdout and exit")
    parser.add('--version', action='version', version=get_version())
    parser.add("--debug", action="store_true",
               help="Print debug messages and dump debug data files")
    parser.add('--paths', action="store_true",
               help="Print config and data paths and exit")
    parser.add('--datadir', default=AppDirs("papersurfer").user_data_dir,
               help='Path to datafiles.')

    options = parser.parse_args()

    config.debug = options.debug

    pathlib.Path(options.datadir).mkdir(parents=True, exist_ok=True)
    config.datadir = options.datadir

    if options.paths:
        print_paths()
        sys.exit(0)

    if not options.url:
        start_interactive = input(
            "Could not load config file or read command line arguments, do you"
            " wish to start the interactive configuration assistant? (y/n) ")
        if start_interactive == "y":
            url, channel, username, password = interactive_configuration()
            try:
                Mattermost(url, channel, username, password)
            except ConfigError:
                print("Failed to validate configuration, exiting.")
                sys.exit(1)

            options.url = url
            options.channel = channel
            options.username = username
            options.password = password
            configpath = AppDirs("papersurfer").user_config_dir

            pathlib.Path(configpath).mkdir(parents=True, exist_ok=True)

            configfile = os.path.join(configpath, "papersurfer.conf")
            with open(configfile, "w") as file:
                file.write(f"url = {url}\n")
                file.write(f"channel = {channel}\n")
                file.write(f"username = {username}\n")
                file.write(f"password = {password}\n")
                print(f"Configfile {configfile} written.")

            time.sleep(2)
        else:
            parser.print_help()
            sys.exit(0)

    return options


def just_posts(url: str, channel: str, username: str, password: str) -> None:
    """Fuck off with all this interactive shit."""
    posts = Papersurfer(url, channel, username, password).get_posts()
    for post in posts:
        print(post.message)


def just_bibtex(url: str, channel: str, username: str, password: str) -> None:
    """Retrieve and dump bibtext formated data, unfiltered."""
    posts = Papersurfer(url, channel, username, password).get_posts()
    dois = [post.doi for post in posts]
    print(Bibtex().bib_from_dois(dois))


def main() -> None:
    """Run main program."""
    opt = parse_args()

    logfile = get_log_file_path()
    pathlib.Path(os.path.dirname(logfile)).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=logfile, level=logging.DEBUG)

    if opt.dump_posts:
        just_posts(opt.url, opt.channel, opt.username, opt.password)
    elif opt.dump_bibtex:
        just_bibtex(opt.url, opt.channel, opt.username, opt.password)
    else:
        PapersurferUi(opt.url, opt.channel, opt.username, opt.password)


if __name__ == "__main__":
    main()
