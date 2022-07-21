import os
from flask import Flask, request
from flask_cors import CORS
import random

app = Flask(__name__)  #opening up app
CORS(app)

#https://www, if we have /generate, send our data to the url
APP_ROOT = os.getenv('APP_ROOT', '/generate')

@app.route(APP_ROOT, methods=["POST"])
def sample_topics():
    data = request.json
    topic_list = data.get('topics')

    sampled = random.sample(topic_list, len(topic_list)-1)


    
    return {'topics':  sampled}
