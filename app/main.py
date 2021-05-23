import logging

from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger()


@app.get("/")
def foobar():
    return {"Hello": "World"}


# urlpatterns = [
#     url(
#         r"^$",
#         lambda request: JsonResponse(
#             {"error": "this bad boy has one whole microservice under the hood"}
#         ),
#         name="base",
#     ),
#     url(r"^(?P<bucket>[a-z0-9\-\_]*)$", views.S3Bucket.as_view(), name="s3_bucket"),
#     url(
#         r"^(?P<bucket>[a-zA-Z0-9\-\_]*)/object$",
#         views.S3Object.as_view(),
#         name="s3_object",
#     ),
#     url(
#         r"^(?P<bucket>[a-zA-Z0-9\-\_]*)/metadata$",
#         views.S3ObjectMetadata.as_view(),
#         name="s3_object_metadata",
#     ),
# ]
