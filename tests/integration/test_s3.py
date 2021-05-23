import json
import logging

import boto3
import pytest

from api import s3


@pytest.mark.postbuild
@pytest.mark.usefixtures("localstack", "s3")
class TestListBucket:
    def test_list_bucket(self, test_bucket, s3_objects):
        n_objects = 5
        objects = []
        for i in range(n_objects):
            objects.append({"key": f"k{i}", "body": {"foo": "bar"}})

        with s3_objects(bucket_name=test_bucket, objects=objects):
            results = s3.list_bucket(bucket_name=test_bucket)
            assert len(results) == n_objects

    def test_list_bucket_paginated(self, test_bucket, s3_objects):
        n_objects = 5
        objects = []
        for i in range(n_objects):
            objects.append({"key": f"k{i}", "body": {"foo": "bar"}})

        with s3_objects(bucket_name=test_bucket, objects=objects):
            results = s3.list_bucket(bucket_name=test_bucket, page=2, page_size=2)
            assert len(results) == 2
            keys = [o["key"] for o in results]
            assert "k2" in keys
            assert "k3" in keys

    def test_list_bucket_sorted(self, test_bucket, s3_objects):
        n_objects = 5
        objects = []
        for i in range(n_objects):
            objects.append({"key": f"k{i}", "body": {"foo": "bar"}})

        with s3_objects(bucket_name=test_bucket, objects=objects):
            results = s3.list_bucket(bucket_name=test_bucket, sorted=True)
            assert len(results) == n_objects
            assert results[0]["key"] == "k4"
            assert results[1]["key"] == "k3"
            assert results[2]["key"] == "k2"
            assert results[3]["key"] == "k1"
            assert results[4]["key"] == "k0"

    def test_list_bucket_sorted_paginated(self, test_bucket, s3_objects):
        n_objects = 5
        objects = []
        for i in range(n_objects):
            objects.append({"key": f"k{i}", "body": {"foo": "bar"}})

        with s3_objects(bucket_name=test_bucket, objects=objects):
            results = s3.list_bucket(
                bucket_name=test_bucket, page=2, page_size=2, sorted=True
            )
            assert len(results) == 2
            assert results[0]["key"] == "k2"
            assert results[1]["key"] == "k1"


@pytest.mark.postbuild
@pytest.mark.usefixtures("localstack", "s3")
class TestGenerateURL:
    def test_generate_presigned_url(self, test_bucket, s3_objects):
        objects = [{"key": "k1", "body": {"foo": "bar"}}]
        with s3_objects(bucket_name=test_bucket, objects=objects):
            url = s3.generate_presigned_url(bucket_name=test_bucket, object_name="k1")
            assert isinstance(url, str)


@pytest.mark.postbuild
@pytest.mark.usefixtures("localstack", "s3")
class TestGetMetadata:
    def test_get_metadata(self, test_bucket):
        metadata = {"wiz": "bang", "ContentType": "foo/bar"}
        client = boto3.client("s3")
        client.put_object(
            Bucket=test_bucket,
            Key="foo",
            Body=json.dumps({"foo": "bar"}).encode(),
            Metadata={"wiz": "bang"},
            ContentType="foo/bar",
        )
        found_metadata = s3.get_object_metadata(
            bucket_name=test_bucket, object_name="foo"
        )
        assert found_metadata == metadata
        client.delete_object(Bucket=test_bucket, Key="foo")
