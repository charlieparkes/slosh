import logging

from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger()


@app.get("/")
def foobar():
    return {"Hello": "World"}
