import boto3_proxy
from django.core.paginator import Paginator


class PermissionError(Exception):
    pass


def flatten_pages(iter):
    try:
        pages = [[o for o in page["Contents"]] for page in iter]
    except KeyError as e:
        raise PermissionError(
            "Received no 'Contents' back from the page iterator. You likely don't have permission to read from this bucket."
        ) from e
    return [o for page in pages for o in page]


def list_bucket(
    bucket_name, page=None, page_size=None, prefix=None, sorted=False, client_kwargs={}
):
    """List object keys in an s3 bucket.

    Args:
        bucket_name (:obj:`str`)
        page (int)
        page_size (int)
        prefix (:obj:`str`, optional): Prefix to filter s3 objects by
        sorted (bool): When true, sorts objects reverse chronologically
        client_kwargs (dict): Additional kwargs to pass to boto3.client()

    Returns:
        list: List of object keys in the s3 bucket

    """

    client = boto3_proxy.client("s3", **client_kwargs)
    paginator = client.get_paginator("list_objects")

    params = {"Bucket": bucket_name}
    if prefix:
        params["Prefix"] = prefix

    pages = paginator.paginate(**params)

    def fmt(o):
        return {"key": o["Key"], "last_modified": o["LastModified"]}

    if sorted:
        objects = flatten_pages(pages)
        objects.sort(key=lambda obj: obj["LastModified"], reverse=True)
        keys = [fmt(o) for o in objects]
    else:
        keys = [fmt(o) for o in flatten_pages(pages)]

    if page and page_size:
        return list(Paginator(keys, page_size).get_page(page))
    else:
        return keys


def generate_presigned_url(bucket_name, object_name, expiration=3600, client_kwargs={}):
    """Generate a presigned URL to share an S3 object.

    Args:
        region (:obj:`str`)
        bucket_name (:obj:`str`)
        object_name (:obj:`str`)
        expiration (int): Time in seconds for the presigned URL to remain valid
        client_kwargs (dict): Additional kwargs to pass to boto3.client()

    Returns:
        str: Presigned URL as string. If error, returns None.

    """

    client = boto3_proxy.client("s3", **client_kwargs)
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expiration,
    )


def get_object_metadata(bucket_name, object_name, client_kwargs={}):
    """Generate a presigned URL to share an S3 object.

    Args:
        region (:obj:`str`)
        bucket_name (:obj:`str`)
        object_name (:obj:`str`)
        client_kwargs (dict): Additional kwargs to pass to boto3.client()

    Returns:
        dict: S3 object metadata

    """

    client = boto3_proxy.client("s3", **client_kwargs)
    o = client.get_object(Bucket=bucket_name, Key=object_name)
    meta = o.get("Metadata", {})
    meta["ContentType"] = o.get("ContentType", "")
    return meta
