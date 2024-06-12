from datetime import datetime
from json import dumps
import re
import urllib.request
from support.aemoconstants import DATE_FORMAT, REGEX_BASEURL, REGEX_ENTRIES, REGEX_LINKS
import html
from dataclasses import dataclass


@dataclass
class Link:
    dt: datetime
    url: str
    depth: int = None
    fileName: str = None
    fileUrl: str = None
    fileSize: int = None
    fileCount: int = 0

    def __post_init__(self):
        self.is_directory = True if self.fileSize is None else False
        self.fileCount = self.fileCount if self.is_directory else None

    def __str__(self):
        tdict = {}
        for k, v in self.__dict__.items():
            if v is None:
                continue
            if type(v) != datetime:
                tdict[k] = v
            else:
                tdict[k] = v.isoformat()

        return dumps(tdict)


@dataclass
class Summary:
    isodate: datetime
    filesize: int
    is_directory: bool


@dataclass
class Anchor:
    href: str
    name: str


def _check_is_aemo_page(contents: str) -> any:
    if "wem.local" not in "".join(re.findall("<title>(.+?)</title>", contents)):
        raise Exception(
            "Unable to find string 'wem.local' in URL title. Are you sure you have the right URL?"
        )


def _fetch_directory_from_url(url: str) -> str:
    response = urllib.request.urlopen(url)
    charset = response.headers.get_content_charset() or "utf-8"
    contents = response.read().decode(charset)
    _check_is_aemo_page(contents)
    return contents


def _extract_dir_entries(content: str) -> list[str]:
    return [row for row in re.findall(REGEX_ENTRIES, html.unescape(content))]


def _create_summary_from_text_block(fstat: str) -> Summary:
    summarylist = [x for x in fstat.split(" ") if x]
    is_dir = True if summarylist[3] == "<dir>" else False
    return Summary(
        isodate=datetime.strptime(
            f"{summarylist[0]} {summarylist[1]} {summarylist[2]}", DATE_FORMAT
        ),
        is_directory=is_dir,
        filesize=int(summarylist[3]) if not is_dir else None,
    )


def _create_anchor_from_text_block(linkcode: str) -> Anchor:
    links = re.findall(REGEX_LINKS, linkcode)
    href = links[0][0]
    anchorname = links[0][1]
    return Anchor(href, anchorname)


def create_dir_entry_objects(url: str, content: str) -> list[Link]:
    entrylinks = []
    base_url = re.sub(REGEX_BASEURL, "\\1", url)
    for row in _extract_dir_entries(content):
        # get the text listing and split the parts by spaces
        summary = _create_summary_from_text_block(fstat=row[0])
        anchor = _create_anchor_from_text_block(linkcode=row[1])
        file_url = (base_url + anchor.href) if not summary.is_directory else None
        final_url = url if not summary.is_directory else base_url + anchor.href
        # url = anchor.href if summary.is_directory else url
        entrylinks.append(
            Link(
                dt=summary.isodate,
                url=final_url,
                fileName=anchor.name if not summary.is_directory else None,
                fileUrl=file_url,
                fileSize=summary.filesize,
            )
        )
    return entrylinks
