#!/usr/bin/env python3

"""
teampulls lists all the open pull requests for the repositories provided in
`repos` for the users specified in `usernames`.
You have to have your Github API token in then environment variable
`GITHUB_TOKEN` or in the config file: github_token = "<your-token>"
"""

__author__ = "Jochen Breuer"
__email__ = "jbreuer@suse.de"
__license__ = "GPLv3"

import os
import sys
import toml
import requests
from functools import partial
from os.path import expanduser
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dateutil import parser
from docopt import docopt
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


__docopt__ = """Usage: teampulls [-hu USER]

-h --help   show this
-u --user   one or many users with comma separated: alice,bob,peter
"""


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_prs_for_user(username, api_token):
    """\
    Fetches the pull requests for the given user and returns
    the data set as a dict.
    """
    query = (
        """
        { user(login: "%s") {
            name
            login
            pullRequests(first: 100, states: OPEN) {
            totalCount
            nodes {
                repository {
                    id
                    nameWithOwner
                }
                isDraft
                baseRefName
                headRefName
                createdAt
                number
                title
                url
            }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }}
        """
        % username
    )
    url = "https://api.github.com/graphql"
    json = {"query": query}
    headers = {
        "Authorization": "token %s" % api_token,
        "Accept": "application/vnd.github.shadow-cat-preview+json",
    }

    r = requests.post(url=url, json=json, headers=headers)
    return r.json()


def get_colour_coding_for_pr(pr, days=14):
    """\
    Returns the colour code needed to print to the CLI.
    The colour is green, unless the pr is > `days` old.
    """
    created_at = parser.parse(pr["createdAt"])
    now = datetime.now(timezone.utc)
    age = now - created_at
    if pr["isDraft"]:
        colour = bcolors.OKBLUE
    else:
        colour = bcolors.OKGREEN
    if age > timedelta(days=days):
        if pr["isDraft"]:
            colour = bcolors.WARNING
        else:
            colour = bcolors.FAIL
    return colour


def get_settings():
    """\
    Loads TOML settings from the provided file and returns a usernames and
    repos. Optionally also the Github API token.
    """
    paths = (
        "./.teampulls.toml",
        "./teampulls.toml",
        "~/.teampulls.toml",
        "~/.config/teampulls.toml",
        "/etc/teampulls.toml",
    )
    settings = None
    for path in paths:
        path = expanduser(path)
        if os.path.isfile(path) and not os.path.isdir(path) and not os.path.islink(path):
            settings = toml.load(path)
            break
    if not settings:
        print(
            "Could not find settings file in any of these locations:\n{}".format(
                "\n".join(paths)
            )
        )
        sys.exit(3)
    if "usernames" not in settings:
        print(
            'usernames definition missing in settings file: usernames = ["bob", "alice"]',
            file=sys.stderr,
        )
        sys.exit(2)
    if "repos" not in settings:
        print(
            'repos definition missing in settings file: repos = ["foo/prj", "bar/prj"]',
            file=sys.stderr,
        )
        sys.exit(2)
    usernames = settings["usernames"]
    repos = settings["repos"]
    github_token = None
    if "github_token" in settings:
        github_token = settings["github_token"]
    return usernames, repos, github_token


def filter_prs_by_repos(pull_requests, repos):
    """\
    Returns only the pull requests that are listed in repos.
    """
    return [
        pull_request
        for pull_request in pull_requests
        if pull_request["repository"]["nameWithOwner"] in repos
    ]


def validate_user_arguments(options):
    """\
    Validates and formats the arguments passed by the user.
    """
    options_users = options.get("USER", None)
    if options_users:
        options_users = [user.strip() for user in options_users.split(",")]

    cleaned_options = {}
    cleaned_options["USERS"] = options_users
    return cleaned_options


def print_prs_detail(data, repos):
    """\
    Printing details of PRs to stdout.
    """
    print("{}{}{}".format(bcolors.OKBLUE, data["data"]["user"]["name"], bcolors.ENDC))
    print("=" * 80)
    pull_requests = filter_prs_by_repos(
        data["data"]["user"]["pullRequests"]["nodes"], repos
    )
    if len(pull_requests) == 0:
        print("No pull requests!\n")
    for i, pr in enumerate(pull_requests):
        title = pr["title"]
        repo = pr["repository"]["nameWithOwner"]
        if repo not in repos:
            continue
        url = pr["url"]
        branch = pr["baseRefName"]
        source_branch = pr["headRefName"]
        print("{}{}{}".format(get_colour_coding_for_pr(pr), title, bcolors.ENDC))
        print("🔗 {}".format(url))
        print("🌿 {} ⟸  {}".format(branch, source_branch))
        if i + 1 == len(pull_requests):
            print("\n")
            continue
        print("-" * 80)


def main():
    options = docopt(__docopt__, help=True)
    cleaned_options = validate_user_arguments(options)
    api_token = None
    config_usernames, repos, api_token = get_settings()
    if not api_token:
        api_token = os.environ.get("GITHUB_TOKEN_GALAXY") or os.environ.get(
            "GITHUB_TOKEN"
        )
    if not api_token:
        print(
            "Please provide a Github API token via environment variable `GITHUB_TOKEN_GALAXY` or via settings file.",
            file=sys.stderr,
        )
        sys.exit(1)

    if cleaned_options["USERS"]:
        # We got a list of users from the cli.
        usernames = cleaned_options["USERS"]
    else:
        # Using users from the config.
        usernames = config_usernames

    get_prs_for_user_with_api_token = partial(get_prs_for_user, api_token=api_token)
    with PoolExecutor(max_workers=8) as executor:
        for data in executor.map(get_prs_for_user_with_api_token, usernames):
            print_prs_detail(data, repos)


if __name__ == "__main__":
    main()
