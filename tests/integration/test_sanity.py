import json

import boto3
import pytest


@pytest.mark.postbuild
@pytest.mark.usefixtures("localstack", "s3")
class TestSanityMockS3:
    def test_mock_s3(self, test_bucket):
        client = boto3.client("s3")
        s3 = boto3.resource("s3")
        assert s3.Bucket(test_bucket) in s3.buckets.all()
        client.put_object(
            Key="foo", Body=json.dumps({"wiz": "bang"}).encode(), Bucket=test_bucket
        )
        client.delete_object(Key="foo", Bucket=test_bucket)

    def test_put_s3_objects(self, test_bucket, s3_objects):
        objects = [
            {"key": "key1", "body": {"foo": "bar"}},
            {"key": "key2", "body": {"wiz": "bang"}},
        ]
        with s3_objects(bucket_name=test_bucket, objects=objects):
            s3 = boto3.resource("s3")
            bucket = s3.Bucket(test_bucket)
            keys = [o.key for o in bucket.objects.all()]
            for o in objects:
                assert o["key"] in keys

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(test_bucket)
        keys = [o.key for o in bucket.objects.all()]
        assert len(keys) == 0
