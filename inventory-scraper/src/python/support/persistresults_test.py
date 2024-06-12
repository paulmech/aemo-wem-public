from support.link import Link
from support.persistresults import write_results_to_s3
from pytest import raises
from datetime import datetime
from unittest.mock import Mock, patch
import gzip
import re


def test_parameter_validation_no_results():
    with raises(Exception) as e:
        write_results_to_s3([], "bucket", "prefix", "request_id", dry_run=True)
    assert e.value.args[0] == "There are no results to write"


def test_parameter_validation_bucket_none():
    with raises(Exception) as e:
        write_results_to_s3([None], None, "prefix", "request_id", dry_run=True)
    assert e.value.args[0] == "A valid bucket name must be specified"


def test_parameter_validation_bucket_empty():
    with raises(Exception) as e:
        write_results_to_s3([None], "", "prefix", "request_id", dry_run=True)
    assert e.value.args[0] == "A valid bucket name must be specified"


def test_parameter_validation_bucket_invalid():
    with raises(Exception) as e:
        write_results_to_s3([None], "bucket_Name", "prefix", "request_id", dry_run=True)
    assert e.value.args[0] == "A valid bucket name must be specified"


def test_parameter_validation_prefix():
    with raises(Exception) as e:
        write_results_to_s3([None], "bucket-name", None, "request_id", dry_run=True)
    assert e.value.args[0] == "A S3 prefix must be specified"


def test_parameter_validation_prefix_empty():
    with raises(Exception) as e:
        write_results_to_s3([None], "bucket-name", "", "request_id", dry_run=True)
    assert e.value.args[0] == "A S3 prefix must be specified"


def test_parameter_validation_arid_none():
    with raises(Exception) as e:
        write_results_to_s3([None], "bucket", "prefix", None, dry_run=True)
    assert e.value.args[0] == "A valid request id is required to de-duplicate runs"


def test_parameter_validation_arid_empty():
    with raises(Exception) as e:
        write_results_to_s3([None], "bucket", "prefix", "", dry_run=True)
    assert e.value.args[0] == "A valid request id is required to de-duplicate runs"


def test_expected_output_path():
    datepart = datetime.now().strftime("%Y-%m-%d")
    output_path = write_results_to_s3(
        [None], "bucket", "prefix///", "my_request_id", dry_run=True
    )
    assert (
        output_path
        == f"s3://bucket/prefix/{datepart}/my_request_id/{datepart}.aemo-inventory.jsonl.gz"
    )


@patch("boto3.client")
def test_s3_upload(s3_client):
    results = [
        Link(url="https://fakeurl.com", dt=datetime.now(), depth=1),
        Link(url="https://fakeurl.com/public/", dt=datetime.now(), depth=2),
    ]
    mock = Mock()
    s3_client.return_value = mock
    mock.upload_fileobj.return_value = True
    thenoo = datetime.now().strftime("%Y-%m-%d")
    upload_path = write_results_to_s3(
        results,
        "aemo-data-ap-southeast-2-111111111111",
        "testing",
        "request_id",
        dry_run=False,
    )
    assert mock.upload_fileobj.called
    assert upload_path.startswith(
        f"s3://aemo-data-ap-southeast-2-111111111111/testing/{thenoo}/request_id/"
    )
    assert upload_path.endswith("aemo-inventory.jsonl.gz")
    original_data = gzip.decompress(mock.upload_fileobj.call_args[0][0].read()).decode(
        "UTF-8"
    )
    assert re.search("{.+?}", original_data)
