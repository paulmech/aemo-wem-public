from support.crawl import crawl_folders
from support.settingscli import Settings
import pytest

TEMPLATE_NO_ENTRIES = """
        <html>
        <head>
            <title>wem.local</title>
        </head>
        <body>
            What uP!
        </body>
        """

TEMPLATE_SINGLE_FILE = """
<html>
        <head>
            <title>wem.local</title>
        </head>
        <body>
            <pre>
                <br>12/13/2023  6:16 AM        83224 <a href="/public/FacilityScada_20230929.zip">FacilityScada_20230929.zip</a>
            </pre>
        </body>
"""

TEMPLATE_ENTRIES_ROOT = """
<html>
        <head>
            <title>wem.local - ROOT</title>
        </head>
        <body>
            <pre>
                <br>12/13/2023  6:16 AM        2712 <a href="/public/somerandomfile.txt">somerandomfile.txt</a>
                <br>1/31/2024  9:52 PM        <dir> <a href="/public/facilityScada/">facilityScada</a>
            </pre>
        </body>
"""
TEMPLATE_ENTRIES_DESCENDENT = """
<html>
        <head>
            <title>wem.local - DESCENDENT</title>
        </head>
        <body>
            <pre>
                <br>12/13/2023  6:16 AM        83224 <a href="/public/facilityScada/FacilityScada_20230929.zip">FacilityScada_20230929.zip</a>
                <br>12/14/2023  6:04 AM        91745 <a href="/public/facilityScada/FacilityScada_20230930.zip">FacilityScada_20230930.zip</a>
            </pre>
        </body>
"""

class Fetcher:
    urls: list
    templates: list

    def __init__(self, templates):
        self.urls = []
        self.templates = templates

    def fetcher(self, url: str):
        self.urls.append(url)
        template = self.templates[0]
        self.templates = self.templates[1:]
        return template
    
def test_crawl_with_fake_url_fetcher():
    fc = Fetcher([TEMPLATE_NO_ENTRIES])
    settings = Settings(["script.py","https://fakeurl.com","list-files"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 1
    assert results[0].is_directory == True
    assert results[0].url == "https://fakeurl.com"
    assert "https://fakeurl.com" in fc.urls

def test_crawl_with_start_url_overrides_default_setting():
    fc = Fetcher([TEMPLATE_NO_ENTRIES])
    settings = Settings(["script.py","https://fakeurl.com","list-files","--start-url","https://override.com"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 1
    assert results[0].is_directory == True
    assert results[0].url == "https://override.com"
    assert "https://fakeurl.com" not in fc.urls
    assert "https://override.com" in fc.urls

def test_crawl_with_discovered_file():
    fc = Fetcher([TEMPLATE_SINGLE_FILE])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 2
    assert results[0].is_directory == True
    assert results[0].url == "https://fakeurl.com/public"

    assert results[1].is_directory == False
    assert results[1].url == "https://fakeurl.com/public"
    assert results[1].fileSize == 83224
    assert results[1].fileName == "FacilityScada_20230929.zip"
    assert results[1].fileUrl == "https://fakeurl.com/public/FacilityScada_20230929.zip"

def test_crawl_with_max_days_old():
    fc = Fetcher([TEMPLATE_SINGLE_FILE])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--max-days-old","30"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 1
    assert results[0].is_directory == True
    assert results[0].url == "https://fakeurl.com/public"

def test_crawl_successful_descendency():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 5
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 1 and link.url == "https://fakeurl.com/public", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 2 and link.url == "https://fakeurl.com/public/facilityScada/", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 2712 and link.fileUrl == "https://fakeurl.com/public/somerandomfile.txt", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 83224 and link.fileUrl == "https://fakeurl.com/public/facilityScada/FacilityScada_20230929.zip", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 91745 and link.fileUrl == "https://fakeurl.com/public/facilityScada/FacilityScada_20230930.zip", results)))

def test_crawl_prohibit_descendency():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--max-depth","1"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 3
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 1 and link.url == "https://fakeurl.com/public", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 0 and link.url == "https://fakeurl.com/public/facilityScada/", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 2712 and link.fileUrl == "https://fakeurl.com/public/somerandomfile.txt", results)))

def test_crawl_prohibit_descendency_no_empty_dirs():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--max-depth","1","--no-empty-dirs"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 2
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 1 and link.url == "https://fakeurl.com/public", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 2712 and link.fileUrl == "https://fakeurl.com/public/somerandomfile.txt", results)))

def test_crawl_max_days_old():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--max-days-old","1"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 2
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 0 and link.url == "https://fakeurl.com/public", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 0 and link.url == "https://fakeurl.com/public/facilityScada/", results)))

def test_crawl_no_recurse():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--no-recurse"])
    results = crawl_folders(settings, fc.fetcher)
    assert len(results) == 3
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 1 and link.url == "https://fakeurl.com/public", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory and link.fileCount == 0 and link.url == "https://fakeurl.com/public/facilityScada/", results)))
    assert 1 == len(list(filter(lambda link: link.is_directory == False and link.fileSize == 2712 and link.fileUrl == "https://fakeurl.com/public/somerandomfile.txt", results)))

def test_curtailment():
    fc = Fetcher([TEMPLATE_ENTRIES_ROOT, TEMPLATE_ENTRIES_DESCENDENT])
    settings = Settings(["script.py","https://fakeurl.com/public","list-files","--no-recurse"])
    with pytest.raises(Exception):
        crawl_folders(settings, fc.fetcher, crawl_limit=1)