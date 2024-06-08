import time
from datetime import datetime, timedelta
from support.aemoconstants import DEFAULT_SLEEPTIME, OPT_MAX_DAY_OLD, OPT_MAX_DEPTH, OPT_NO_EMPTY_DIRS, OPT_NO_RECURSE, OPT_SLEEPTIME, OPT_URL
from support.settingscli import Settings
from support.link import Link, _fetch_directory_from_url, create_dir_entry_objects

DEFAULT_CRAWL_LIMIT = 500
def single_number(args: list[str],isFloat=False) -> int:
    return int("".join(args)) if not isFloat else float("".join(args))

def crawl_folders(settings: Settings, fetcher: any = _fetch_directory_from_url, crawl_limit: int = DEFAULT_CRAWL_LIMIT):
    url = settings.url if OPT_URL not in settings.options else settings.options[OPT_URL][0]
    sleeptime = DEFAULT_SLEEPTIME if not OPT_SLEEPTIME in settings.options else single_number(settings.options[OPT_SLEEPTIME],True)

    thenoo = datetime.now()
    thenoo = thenoo.replace(microsecond=0)
    all_dirs = [ Link( dt=thenoo, url=url, depth=1 ) ]
    discovered = []
    current_position = 0

    while current_position < crawl_limit and current_position < len(all_dirs):
        current_dir = all_dirs[current_position]
        current_url = current_dir.url
        current_depth = current_dir.depth
        if OPT_MAX_DEPTH in settings.options and single_number(settings.options[OPT_MAX_DEPTH]) < current_depth:
            current_position += 1
            continue
        time.sleep(sleeptime)
        # retrieve content from the URL
        contents = fetcher( current_url )
        # parse content to list of directory entries
        dir_entries = create_dir_entry_objects(url=current_url, content=contents)
        # loop over each directory entry
        for entry in dir_entries:
            if entry.is_directory:
                if OPT_NO_RECURSE in settings.options or \
                    OPT_MAX_DEPTH in settings.options and single_number(settings.options[OPT_MAX_DEPTH]) < current_depth:
                    discovered.append(entry)
                    continue
                entry.depth = current_depth + 1
                all_dirs.append( entry )
            else:
                if OPT_MAX_DAY_OLD in settings.options and entry.dt < (datetime.now() - timedelta(days= single_number(settings.options[OPT_MAX_DAY_OLD]))):
                    continue
                entry.depth = current_depth
                discovered.append( entry )
                current_dir.fileCount += 1
        # increment the current position to read from the all_dirs work tracker
        current_position += 1

    if crawl_limit == current_position:
        raise Exception(f"Reached crawl limit of {crawl_limit} directories")
    # combine the results of directories descended, discovered files, and directories discovered but not descended
    discovered = all_dirs + discovered

    # filter empty directories from listing if requested
    if ( OPT_NO_EMPTY_DIRS in settings.options ):
        discovered = list(filter(lambda item: item.is_directory and item.fileCount > 0 or not item.is_directory, discovered))

    for item in discovered:
        item._created_at = thenoo
    return discovered