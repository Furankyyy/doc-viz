import os

import dash
import dash_bootstrap_components as dbc
import flask
import redis
from rq import Queue

server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(server=server, external_stylesheets=external_stylesheets,  serve_locally=False)

# redis connection and RQ queue. use redistogo service when dpeloying to Heroku
redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)
