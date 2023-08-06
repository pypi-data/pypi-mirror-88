# Copyright Greg Werbin, 2020
#
# This file is part of TSQuery.
#
# TSQuery is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TSQuery is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TSQuery.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import annotations

import logging
from pathlib import Path
from typing import Generator, Iterable, Sequence

import attr
import tree_sitter as ts

from tsquery.xdg import get_xdg_dirs, get_xdg_home


logger = logging.getLogger(__name__)


TSTuple = tuple[ts.Language, ts.Parser]


DEFAULT_PARSER_PATHS = (
    get_xdg_home('XDG_DATA_HOME') / 'tree-sitter/parsers',
    *(d / 'tree-sitter/parsers' for d in get_xdg_dirs('XDG_DATA_DIRS'))
)


def iter_available_parsers(parser_paths: Iterable[Path]) -> Generator[Path, None, None]:
    for path in parser_paths:
        if path.is_dir():
            for f in path.iterdir():
                if f.suffix == '.so':
                    yield f


def list_available_parsers(parser_paths: Iterable[Path]) -> list[Path]:
    return list(iter_available_parsers(parser_paths))


def new_parser(language: ts.Language) -> ts.Parser:
    parser = ts.Parser()
    parser.set_language(language)
    return parser


def load_parser(name: str, file: Path) -> TSTuple:
    language = ts.Language(str(file), name)
    return language, new_parser(language)


class ParserUnavailable(Exception):
    parser_name: str
    expected_filename: str

    def __init__(self, parser_name: str, expected_filename: str):
        self.parser_name = parser_name
        self.expected_filename = expected_filename

    def __str__(self) -> str:
        return f'Could not locate file "{self.expected_filename}" for language "{self.parser_name}".'


@attr.s
class ParserRegistry:
    parsers: dict[str, TSTuple]
    parser_paths: Sequence[Path] = attr.ib(default=DEFAULT_PARSER_PATHS)

    def __attrs_post_init__(self):
        self.parsers = {}
        logger.debug('Using paths: %s', ' : '.join(map(str, self.parser_paths)))

    def iter_available(self) -> Generator[Path, None, None]:
        return iter_available_parsers(self.parser_paths)

    def list_available(self) -> list[Path]:
        return list_available_parsers(self.parser_paths)

    def find_parser_file(self, name: str) -> Path:
        expected_filename = f'{name}.so'
        logger.debug('For language "%s", searching for parser file "%s"', name, expected_filename)
        for f in self.iter_available():
            logger.debug('For language "%s", trying %s', name, f)
            if f.name == expected_filename:
                logger.debug('For language "%s", returning %s', name, f)
                return f
        else:
            raise ParserUnavailable(name, expected_filename)

    def _load(self, name: str) -> TSTuple:
        parser_file = self.find_parser_file(name)
        language, parser = load_parser(name, parser_file)
        self.parsers[name] = language, parser
        return language, parser

    def get(self, name: str, force_reload: bool = False) -> TSTuple:
        if force_reload:
            result = self._load(name)
        else:
            result_maybe = self.parsers.get(name, None)
            if result_maybe is None:
                result = self._load(name)
            else:
                logger.debug('For language "%s", getting language & parser from cache', name)
                result = result_maybe
        return result

    def query(self, lang_name: str, query_text: str, source: bytes) -> list[tuple[ts.Node, str]]:
        language, parser = self.get(lang_name)
        tree = parser.parse(source)
        query = language.query(query_text)
        captures = query.captures(tree.root_node)
        return captures

