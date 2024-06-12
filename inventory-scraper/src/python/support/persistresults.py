from support.link import Link
from datetime import datetime
import boto3
import re
from io import BytesIO
import gzip


def write_results_to_s3(
    results: list[Link],
    bucket: str,
    prefix: str,
    aws_request_id: str,
    dry_run: bool = False,
) -> str:
    # calculate the output filename
    if len(results) == 0:
        raise Exception("There are no results to write")
    elif (
        bucket is None
        or len(bucket) == 0
        or re.search("[^a-z0-9\\-\\.]", bucket) is not None
    ):
        raise Exception("A valid bucket name must be specified")
    elif prefix is None or len(prefix) == 0:
        raise Exception("A S3 prefix must be specified")
    elif aws_request_id is None or len(aws_request_id) == 0:
        raise Exception("A valid request id is required to de-duplicate runs")

    # what time is it now
    thenoo = datetime.now().isoformat()[:10]
    # strip any leading slashes
    bucket_key = re.sub("(.+?)(/+)?$", "\\1/", prefix)
    # add the timestamp and request id
    bucket_key += f"{thenoo}/{aws_request_id}"
    # add the filename component
    bucket_key += f"/{thenoo}.aemo-inventory.jsonl.gz"

    # if not dry run, save to S3
    if not dry_run:
        resultstream = "\n".join([str(link) for link in results]) + "\n"
        upload_text_to_s3_gzip_file(resultstream, bucket, bucket_key)
    return f"s3://{bucket}/{bucket_key}"


def upload_text_to_s3_gzip_file(content: str, bucket: str, key: str):
    s3 = boto3.client("s3")
    bs = content.encode(encoding="UTF-8")
    gs = gzip.compress(bs)
    bio = BytesIO(gs)
    s3.upload_fileobj(bio, bucket, key)
