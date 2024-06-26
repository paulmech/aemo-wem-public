REGEX_ENTRIES = "(?i)(?:<br>)+(.+?)?(<a.+?</a>)"
REGEX_LINKS = '(?i)href="(.+?)".*?>(.+)</a>'
REGEX_BASEURL = "^(https://.[^/]+)/.*"
DATE_FORMAT = "%m/%d/%Y %I:%M %p"
MANIFEST_PATH = "public-data/manifests/"
OPT_MAX_DAY_OLD = "max-days-old"
OPT_MIN_DAY_OLD = "min-days-old"
OPT_NO_RECURSE = "no-recurse"
OPT_MAX_DEPTH = "max-depth"
OPT_NO_EMPTY_DIRS = "no-empty-dirs"
OPT_URL = "start-url"
OPT_SLEEPTIME = "sleep-time"
DEFAULT_SLEEPTIME = 0.5
ACCEPTED_COMMANDS = ["list-files"]
ENV_AEMOWEM_URL = "AEMOWEM_URL"
ENV_AEMOWEM_BUCKET = "AEMOWEM_BUCKET"
ENV_AEMOWEM_PREFIX = "AEMOWEM_PREFIX"
LAMBDA_EVENT_OPTIONS = "options"
