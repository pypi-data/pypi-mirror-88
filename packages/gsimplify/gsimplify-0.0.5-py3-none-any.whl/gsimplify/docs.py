import collections
import pprint
from typing import List, Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from jinja2 import Template
from pydantic import BaseModel

from gsimplify.build import Builder
from gsimplify.typedefs import DocType, FolderType, Drive

DEPTH_LEVELS = ["TITLE", "HEADING_1", "HEADING_2", "HEADING_3", "NORMAL_TEXT"]
HTML_DEPTH_LEVELS = ["h1", "h2", "h3", "h4", "p"]


class Docs:
    def __init__(self, doc: DocType, creds, navbar_items: List[Tuple[str, str]] = None, builder: Builder = None):
        self.document = doc
        self.service = build("docs", "v1", credentials=creds)
        self.get(doc.id)

        self.navbar_items = navbar_items
        if self.navbar_items is None:
            self.navbar_items = []

        self.builder = builder

        self.document.ast = self.parse()

    def __str__(self):
        return pprint.pformat(self.document)

    def __repr__(self):
        return str(self)

    def render(self, template: Template) -> str:
        html_tree = self.ast_to_html_tree(self.document.ast)
        return template.render(**self.document.dict(), html_tree=html_tree, navbar_items=self.navbar_items)

    def get(self, id=str) -> dict:
        """
        Grabs the document from Google Docs
        """
        self.document.content = self.service.documents().get(documentId=id).execute()
        return self.document.content

    def parse(self):
        """
        Parses document into a dict-like parse tree.
        """
        ast = self.test_parse(self.document.content.get("body").get("content"))
        self.document.title = ast[0][0]

        return ast

    def recursive_parse(self, structure: list, depth=0) -> dict:
        HTML_DEPTH_LEVELS = [""]

        """
        Recursive/monadic parser.
        """
        level = DEPTH_LEVELS[depth]
        ast = collections.OrderedDict()
        pretext = []
        posttext = []
        count = 0
        for outer_count, section in enumerate(structure):
            stop_loop = True
            if "paragraph" in section:
                paragraph = section.get("paragraph")
                style = paragraph.get("paragraphStyle").get("namedStyleType")
                if style == level:
                    content = "".join(
                        [
                            elm.get("textRun").get("content")
                            for elm in paragraph.get("elements")
                        ]
                    )

                    stop_count = 0
                    for inner_count, lookahead_section in enumerate(
                        structure[count + 1 :]
                    ):
                        if "paragraph" in lookahead_section:
                            inner_style = (
                                lookahead_section.get("paragraph")
                                .get("paragraphStyle")
                                .get("namedStyleType")
                            )
                            if (
                                inner_style == style and stop_count == 0
                            ):  # first encounter of equal depth
                                stop_count = inner_count
                                stop_loop = False
                                break
                    else:
                        stop_count = len(structure)

                    if count:
                        pretext = self.recursive_parse(structure[:count], depth=depth)
                    else:
                        pretext = collections.OrderedDict()

                    if count + 1 - stop_count:
                        posttext = self.recursive_parse(
                            structure[count + 1 : stop_count], depth=depth
                        )
                    else:
                        posttext = collections.OrderedDict()

                    ast[content] = (pretext, posttext)

                    if stop_loop:  # done
                        break
                    else:  # next elements are equal depth
                        del structure[:stop_count]
                        count = 0
                        continue  # skip the count incrementer
            count += 1
        else:
            if depth + 1 < len(DEPTH_LEVELS):
                ast[""] = (
                    collections.OrderedDict(),
                    self.recursive_parse(structure, depth=depth + 1),
                )
        return ast

    def test_parse(self, structure: list) -> List[Tuple[str, List]]:
        ast = []

        for section in structure:
            if "paragraph" not in section:
                continue

            paragraph = section.get("paragraph")
            style: str = paragraph.get("paragraphStyle").get("namedStyleType")

            def text_run_to_str(text_run: dict) -> str:
                if "link" in text_run["textStyle"]:
                    link = text_run["textStyle"]["link"]["url"]
                    if self.builder is not None:
                        link = self.builder.adjust_relative_link(link)
                    return f'<a href="{link}">{text_run["content"]}</a>'
                return text_run['content']

            content = "".join(
                [text_run_to_str(elm.get("textRun")) for elm in paragraph.get("elements")]
            ).rstrip()

            if len(content) < 1:
                continue

            depth_level = DEPTH_LEVELS.index(style)

            relative_depth_level = depth_level
            ast_slice = ast
            while relative_depth_level > 0:
                relative_depth_level -= 1
                if len(ast_slice) == 0:
                    ast_slice.append((None, []))
                ast_slice = ast_slice[-1][1]

            ast_slice.append((content, []))

        assert len(ast) == 1

        return ast

    def ast_to_html_tree(self, ast: List[Tuple[str, List]], depth=0):
        sectioned_levels = ["h2"]
        section_start = '<section>'
        section_end = '</section>'

        result = []

        for section in ast:
            if section[0] is None:
                result += self.ast_to_html_tree(section[1], depth+1)
                continue

            text_type = HTML_DEPTH_LEVELS[depth]
            sectioned = text_type in sectioned_levels

            if sectioned:
                result.append(section_start)

            result.append(f"<{text_type}>{section[0]}</{text_type}>")

            if text_type == "h1":
                result.append('<div class="main">')

            result += self.ast_to_html_tree(section[1], depth+1)

            if text_type == "h1":
                result.append('</div>')

            if sectioned:
                result.append(section_end)

        return result
