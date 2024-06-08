from datetime import datetime
from json import dumps
from support.aemoconstants import (DEFAULT_SLEEPTIME, ACCEPTED_COMMANDS)

class Settings:
    def __init__(self, args: list[str]):
        self.sleeptime = DEFAULT_SLEEPTIME
        if len(args) == 0:
            raise Exception("No arguments provided")
        elif type(args) is not list:
            raise Exception("Expected a list of string parameters")

        if args[0].lower().endswith(".py"):
            args = args[1:]
        else:
            raise Exception("Expected python script name")

        if len(args) > 0:
            self.url= args[0]
            if not (self.url.startswith("http://") or self.url.startswith("https://")):
                raise Exception(f"URL does not meet expectations: {self.url}")
            args = args[1:]
        else:
            raise Exception("URL expected")

        if len(args) > 0 and args[0].lower() in ACCEPTED_COMMANDS:
            self.command = args[0]
            args = args[1:]
        else:
            raise Exception(f"Unknown command: expected one from {ACCEPTED_COMMANDS}")

        self.options = {}

        currentOption = None
        while len(args) > 0:
            if args[0].startswith("--"):
                currentOption = args[0][2:]
                self.options[currentOption] = []
            elif currentOption != None:
                self.options[currentOption].append(args[0])
            args = args[1:]

def help(): # pragma: no cover    
    print("""
    AEMO WEM Data Utility
    (Also known Aemo Wemdu, pronounced Mace Windu)

    Usage:

    aemo-wem <url> <command> <options>

    URL:
        currently should be https://data.wa.aemo.com.au/public/
        it is required to generate fully qualified URLs

    COMMANDS:
        list-files


    OPTIONS:
        --max-days-old <int>    - only consider files newer than <int> days old
        --min-days-old <int>    - only consider files older than <int> days old
        --no-recurse            - do not recurse into child directories
        --max-depth    <int>    - do not descend further than <int> directories
        --start-url    <str>    - custom URL to begin from
        --no-empty-dirs         - don't return directories that didn't have any files at their relative depth

        """)