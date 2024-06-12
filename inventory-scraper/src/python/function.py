import sys
import os
from support.aemoconstants import (
    ENV_AEMOWEM_BUCKET,
    ENV_AEMOWEM_PREFIX,
    ENV_AEMOWEM_URL,
    LAMBDA_EVENT_OPTIONS,
)
from support.settingscli import Settings, help
from support.crawl import crawl_folders
from support.persistresults import write_results_to_s3


def create_settings(event, context):
    args = ["lambda_function.py"]
    if ENV_AEMOWEM_URL in os.environ:
        args.append(os.environ[ENV_AEMOWEM_URL])
    else:
        raise Exception(
            f"No URL was provided in environment variable {ENV_AEMOWEM_URL}"
        )
    args = args + ["list-files"]

    # allow setting parameters from lambda event object
    if event is not None and LAMBDA_EVENT_OPTIONS in event:
        for setting in event[LAMBDA_EVENT_OPTIONS]:
            args.append(setting if setting.startswith("--") else f"--{setting}")
            raw = str(event[LAMBDA_EVENT_OPTIONS][setting])
            args = args + [raw] if type(raw) != "list" else raw

    return Settings(args)


def lambda_handler(event, context):
    settings = create_settings(event, context)
    bucket = os.environ[ENV_AEMOWEM_BUCKET]
    prefix = os.environ[ENV_AEMOWEM_PREFIX]
    aws_request_id = context.aws_request_id
    e = execute(settings, bucket, prefix, aws_request_id)
    if e:
        raise e


def execute(
    settings: Settings,
    bucket: str = None,
    prefix: str = None,
    aws_request_id: str = None,
):
    try:
        results = crawl_folders(settings)
        if bucket and prefix and aws_request_id:
            write_results_to_s3(results, bucket, prefix, aws_request_id)
        else:
            for result in results:
                print(result)
    except Exception as e:
        print(f"ERROR: {e}")
        help()
        return e


if __name__ == "__main__":
    try:
        execute(Settings(sys.argv))
    except Exception as e:
        print(e)
        help()
