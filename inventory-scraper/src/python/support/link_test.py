from datetime import datetime
from support.link import (Link, _check_is_aemo_page, _create_summary_from_text_block, _create_anchor_from_text_block, _fetch_directory_from_url, create_dir_entry_objects)
from json import loads
from unittest.mock import patch, Mock
import pytest

def test_link_conversion():
    dt = datetime.now()
    link = Link(dt=dt, url="https://data.wa.aemo.com.au")
    
    arr = loads(str(link))
    assert arr["dt"] == dt.isoformat()
    assert arr["is_directory"] == True

def test_link_is_not_dir_when_filesize_specified():
    dt = datetime.now()
    link = Link(dt, url="https://data.wa.aemo.com.au", fileSize=50)
    assert not link.is_directory

def test_check_aemo_page_true():
    content = """<html><head><title>NORREWMWAPP1.wem.local - /public/</title>"""
    _check_is_aemo_page(content)
    

def test_check_aemo_page_false():
    content = """<html><head><title>Something much funny in the world</title>"""
    with pytest.raises(Exception):
        _check_is_aemo_page(content)

def test_parse_of_summary_directory():
    text = " 4/22/2021  3:59 PM        <dir> 20140701 "
    summary = _create_summary_from_text_block(text)
    assert summary.is_directory
    assert summary.isodate.isoformat()[:16] == "2021-04-22T15:59"

def test_parse_of_summary_file():
    text = " 4/22/2024  8:01 PM        2398 web.config "
    summary = _create_summary_from_text_block(text)
    assert not summary.is_directory
    assert summary.isodate.isoformat()[:16] == "2024-04-22T20:01"
    assert summary.filesize == 2398

def test_anchor_parse_one():
    anchor = _create_anchor_from_text_block("""<a href="/scoobydoo" class="ng-angular">This is my text!</a>  ayye yo""")
    assert anchor.name == "This is my text!"
    assert anchor.href == "/scoobydoo"

def test_create_links_from_content():
    content = """
 <br>4/22/2021  1:59 PM        <dir> <a href="/scoobydoo1/dir1" class="ng-angular">link one</a> 
 <br>6/22/2025  3:59 PM        <dir> <a href="/scoobydoo1/dir2" class="ng-angular">link two</a> 
 <br>8/22/2029  5:59 PM        319424 <a href="/scoobydoo1/myfilename.txt" class="ng-angular">link three</a> 
    """
    links = create_dir_entry_objects("https://data.wa.aemo.com.au/scoobydoo1", content)
    assert len(links) == 3
    assert links[0].is_directory
    assert links[0].dt.isoformat()[:16] == "2021-04-22T13:59"
    assert links[0].url == "https://data.wa.aemo.com.au/scoobydoo1/dir1"
    assert links[0].fileCount == 0

    assert links[1].is_directory
    assert links[1].dt.isoformat()[:16] == "2025-06-22T15:59"
    assert links[1].url == "https://data.wa.aemo.com.au/scoobydoo1/dir2"
    assert links[1].fileCount == 0

    assert not links[2].is_directory
    assert links[2].dt.isoformat()[:16] == "2029-08-22T17:59"
    assert links[2].url == "https://data.wa.aemo.com.au/scoobydoo1"
    assert links[2].fileUrl == "https://data.wa.aemo.com.au/scoobydoo1/myfilename.txt"
    assert links[2].fileName == "link three"
    assert links[2].fileSize == 319424
    assert links[2].fileCount == None

@patch('urllib.request.urlopen')
def test_fetch_url(mymock):
    reader = Mock()
    decoder = Mock()
    mymock.return_value.headers.get_content_charset = lambda : None
    mymock.return_value.read = reader
    reader.return_value.decode = decoder
    decoder.return_value = """
    <title>wem.local</title>
    """
    response = mymock.return_value
    content = _fetch_directory_from_url("https://fakeurl.com")
    assert len(content) > 0
