import logging

import botocore
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import s3
from api.payload import InvalidPayload, Param, validate_payload
from api.utils import Timer

AWS_DEFAULT_REGION = "us-east-2"

logger = logging.getLogger()


def _build_error_response(exception, params=None, took=None, status=500):
    payload = {"error": f"{exception}"}
    if params:
        payload["params"] = params
    if took:
        payload["took"] = took
    return JsonResponse(payload, status=status)


class S3Bucket(PermissionRequiredMixin, View):
    """List contents of a bucket.

    URL Parameters:
    * bucket: S3 bucket name

    GET Parameters:
    * region (str): optional, AWS region
    * page (int): optional, desired page
    * page_size (int): optional, size of page
    * prefix (str): optional, prefix to filter s3 objects by
    * sorted (bool): optional, sorts objects by last modified, reverse chronologically

    Examples:
        GET /my-bucket

    """

    permission_required = "bucketapi"
    raise_exception = False

    def get(self, request, **kwargs):
        timer = Timer()
        response = {}
        try:
            payload = request.GET.dict()
            payload.update(kwargs)
            params = validate_payload(
                payload,
                {
                    "bucket": Param(str, required=True),
                    "region": Param(str, required=False, default=AWS_DEFAULT_REGION),
                    "page": Param(int, required=False, default=1),
                    "page_size": Param(int, required=False, default=10),
                    "prefix": Param(str, required=False),
                    "sorted": Param(bool, required=False),
                },
            )
            if settings.DEBUG:
                response["debug"] = {"params": params}
        except InvalidPayload as e:
            return _build_error_response(f"Invalid payload: {e}", status=400)

        try:
            response["data"] = s3.list_bucket(
                bucket_name=params["bucket"],
                page=params["page"],
                page_size=params["page_size"],
                prefix=params["prefix"],
                sorted=params["sorted"],
                client_kwargs={"region_name": params["region"]},
            )
        except s3.PermissionError as e:
            return _build_error_response(e, params, timer.stop(), 403)

        response["page"] = params["page"]
        response["page_size"] = params["page_size"]
        response["took"] = timer.stop()
        return JsonResponse(response)


class S3Object(PermissionRequiredMixin, View):
    """Given an S3 bucket and key, return a redirect to a presigned URL

    URL Parameters:
    * region (str): optional, AWS region

    Examples:
        GET /my-bucket/1234%2F5678

    """

    permission_required = "bucketapi"
    raise_exception = False

    def get(self, request, **kwargs):
        timer = Timer()
        response = {}
        try:
            payload = request.GET.dict()
            payload.update(kwargs)
            params = validate_payload(
                payload,
                {
                    "bucket": Param(str, required=True),
                    "key": Param(str, required=True),
                    "region": Param(str, required=False, default=AWS_DEFAULT_REGION),
                    "redirect": Param(bool, required=False, default=True),
                },
            )
            if settings.DEBUG:
                response["debug"] = {"params": params}
        except InvalidPayload as e:
            return _build_error_response(f"Invalid payload: {e}", status=400)

        try:
            response["url"] = s3.generate_presigned_url(
                bucket_name=params["bucket"],
                object_name=params["key"],
                client_kwargs={"region_name": params["region"]},
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return _build_error_response(
                    f"Unable to find {key} in {bucket}.", params, status=404
                )
            raise

        if params["redirect"]:
            return HttpResponseRedirect(response["url"])

        response["took"] = timer.stop()
        return JsonResponse(response)


class S3ObjectMetadata(PermissionRequiredMixin, View):
    """Given an S3 bucket and key, return the object's metadata

    URL Parameters:
    * region (str): optional, AWS region

    Examples:
        GET /my-bucket/1234%2F5678/metadata

    """

    permission_required = "bucketapi"
    raise_exception = False

    def get(self, request, **kwargs):
        response = {}
        try:
            payload = request.GET.dict()
            payload.update(kwargs)
            params = validate_payload(
                payload,
                {
                    "bucket": Param(str, required=True),
                    "key": Param(str, required=True),
                    "region": Param(str, required=False, default=AWS_DEFAULT_REGION),
                },
            )
            if settings.DEBUG:
                response["debug"] = {"params": params}
        except InvalidPayload as e:
            return _build_error_response(f"Invalid payload: {e}", status=400)

        try:
            meta = s3.get_object_metadata(
                bucket_name=params["bucket"],
                object_name=params["key"],
                client_kwargs={"region_name": params["region"]},
            )

            meta["url"] = s3.generate_presigned_url(
                bucket_name=params["bucket"],
                object_name=params["key"],
                client_kwargs={"region_name": params["region"]},
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return _build_error_response(
                    f"Unable to find {key} in {bucket}.", params, status=404
                )
            raise

        response.update(meta)
        return JsonResponse(response)
