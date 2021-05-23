import json
from contextlib import contextmanager

import boto3
import pytest
import pytest_localstack


localstack = pytest_localstack.patch_fixture(
    services=["s3"], scope="class", autouse=False
)


@pytest.fixture(scope="class")
def test_bucket():
    return "test-bucket"


@pytest.fixture(scope="class")
def s3(test_bucket):
    client = boto3.client("s3")
    client.create_bucket(Bucket=test_bucket)


@pytest.fixture
def s3_objects():
    @contextmanager
    def put(bucket_name, objects):
        client = boto3.client("s3")
        try:
            for o in objects:
                client.put_object(
                    Bucket=bucket_name,
                    Key=o["key"],
                    Body=json.dumps(o["body"]).encode(),
                )
            yield
        finally:
            for o in objects:
                client.delete_object(Bucket=bucket_name, Key=o["key"])

    return put
