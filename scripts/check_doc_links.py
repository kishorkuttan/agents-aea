#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Script to check that all internal doc links are valid."""

import re
import sys
from pathlib import Path
from typing import Pattern, Set

import requests

LINK_PATTERN_MD = re.compile(r"\[([^]]+)]\(\s*([^]]+)\s*\)")
LINK_PATTERN = re.compile(r'(?<=<a href=")[^"]*')
IMAGE_PATTERN = re.compile(r'<img[^>]+src="([^">]+)"')
RELATIVE_PATH_STR = "../"
RELATIVE_PATH_STR_LEN = len(RELATIVE_PATH_STR)
INDEX_FILE_PATH = Path("docs/index.md")

WHITELIST_URL_TO_CODE = {
    "http://soef.fetch.ai:9002": 405,
    "https://golang.org/dl/": 403,
    "https://www.wiley.com/en-gb/An+Introduction+to+MultiAgent+Systems%2C+2nd+Edition-p-9781119959519": 403,
    "https://colab.research.google.com": 403,
}


def is_url_reachable(url: str) -> bool:
    """
    Check if a url is reachable.

    :param url: the url to check
    :return: bool
    """
    if url.startswith("http://localhost") or url.startswith("http://127.0.0.1"):
        return True
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        elif response.status_code in [403, 405]:
            return WHITELIST_URL_TO_CODE.get(url, 404) in [403, 405]
        else:
            return False
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return False


def check_header_in_file(header: str, file: Path) -> None:
    """
    Check if the string is present in the file.

    :param header: the header
    :param file: the file path
    """
    with open(file) as f:
        s = f.read()
        if header not in s:
            raise ValueError(
                "Header={} not found in file={}!".format(header, str(file))
            )


def validate_internal_url(file: Path, url: str, all_files: Set[Path]) -> None:
    """
    Validate whether the url is a valid path to a file in docs.

    :param file: the file path
    :param url: the url to check
    :param regex: the regex to check for in the file.
    :return: None
    """
    is_index_file = file == INDEX_FILE_PATH

    if not url.startswith(RELATIVE_PATH_STR) and not is_index_file:
        raise ValueError("Invalid relative path={} in file={}!".format(url, str(file)))

    md_index = url.find(".md")
    if md_index != -1:
        raise ValueError(
            "Path={} contains invalid `.md` in file={}!".format(url, str(file))
        )

    hash_index = url.find("#")
    if hash_index == -1:
        n_url = url[RELATIVE_PATH_STR_LEN:] if not is_index_file else url
        n_url = n_url[:-1] if n_url[-1] == "/" else n_url
        path = Path("docs/{}.md".format(n_url))
        header = ""
    else:
        n_url = url[RELATIVE_PATH_STR_LEN:hash_index] if not is_index_file else url
        n_url = n_url[:-1] if n_url[-1] == "/" else n_url
        path = Path("docs/{}.md".format(n_url))
        header = url[hash_index:]

    if path not in all_files:
        raise ValueError(
            "Path={} found in file={} does not exist!".format(str(path), str(file))
        )

    if header != "":
        check_header_in_file(header, file)


def _checks_all_html(file: Path, regex: Pattern = LINK_PATTERN_MD) -> None:
    """
    Checks a file for matches to a pattern.

    :param file: the file path
    :param all_files: all the doc file paths
    :param regex: the regex to check for in the file.
    """
    matches = regex.finditer(file.read_text())
    for _ in matches:
        raise ValueError("Markdown link found in file={}!".format(str(file)))


def _checks_link(
    file: Path, all_files: Set[Path], regex: Pattern = LINK_PATTERN
) -> None:
    """
    Checks a file for matches to a pattern.

    :param file: the file path
    :param all_files: all the doc file paths
    :param regex: the regex to check for in the file.
    """
    matches = regex.finditer(file.read_text())
    for match in matches:
        result = match.group()
        if result.startswith("https") or result.startswith("http"):
            if not is_url_reachable(result):
                raise ValueError(
                    "Could not reach url={} in file={}!".format(result, str(file))
                )
        else:
            validate_internal_url(file, result, all_files)


def _checks_image(file: Path, regex: Pattern = IMAGE_PATTERN) -> None:
    """
    Checks a file for matches to a pattern.

    :param file: the file path
    :param all_files: all the doc file paths
    :param regex: the regex to check for in the file.
    """
    matches = regex.finditer(file.read_text())
    for match in matches:
        result = match.group(1)

        png_index = result.find(".png")
        if png_index != -1:
            img_path = Path("docs/{}".format(result[RELATIVE_PATH_STR_LEN:]))
            if not img_path.exists():
                raise ValueError(
                    "Image path={} in file={} not found!".format(img_path, str(file))
                )
            return
        elif result.startswith("https") or result.startswith("http"):
            if not is_url_reachable(result):
                raise ValueError(
                    "Could not reach url={} in file={}!".format(result, str(file))
                )
        else:
            raise ValueError("Image path={} in file={} not `.png`!")


def check_file(file: Path, all_files: Set[Path]) -> None:
    """
    Check the links in the file.

    :param file: the file path
    :param all_files: all the doc file paths
    :return: None
    """
    _checks_all_html(file)
    _checks_link(file, all_files)
    _checks_image(file)


def get_all_docs_files() -> Set[Path]:
    """
    Get all file paths to docs or api docs.

    :return: list of all paths
    """
    all_files = Path("docs").glob("**/*.md")
    return set(all_files)


if __name__ == "__main__":
    all_docs_files = get_all_docs_files()
    docs_files = Path("docs").glob("*.md")

    try:
        for file in docs_files:
            print("Processing " + str(file))
            check_file(file, all_docs_files)
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        sys.exit(1)

    print("Done!")
    sys.exit(0)
