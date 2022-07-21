import os
from flask import Flask, request
from flask_cors import CORS
import random
import pandas as pd

app = Flask(__name__)  #opening up app
CORS(app)

#load data
df = pd.read_csv('../data/data.csv')

#https://www, if we have /generate, send our data to the url
APP_ROOT = os.getenv('APP_ROOT', '/generate')

@app.route(APP_ROOT, methods=["POST"])
def generate_pastpaper():
    data = request.json
    topic_list = data.get('topics')

    topic_df = df[df['topic'].isin(topic_list)]

    componenet2 = topic_df[topic_df['comment' == 2]]
    componenet4 = topic_df[topic_df['comment' == 2]]
    componenet6 = topic_df[topic_df['comment' == 2]]
    
    images = {
        'component2'['screenshot_path'].to_list(),
        'component4'['screenshot_path'].to_list(),
        'component6'['screenshot_path'].to_list()

    }

    


    sampled = random.sample(topic_list, len(topic_list)-1)




    
    return {'topics':  sampled}
