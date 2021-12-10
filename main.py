from flask import Flask

from db import db_init

app=Flask(__name__)


@app.route('/')

def hello_world():
    return "hello, world"

