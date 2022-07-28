import os
from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

from app.save_to_pdf import process_pdf

app = Flask(__name__)  #opening up app
CORS(app)

cred = credentials.Certificate('igcse-predict-c18eb87031fd.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'igcse-predict.appspot.com'})

bucket = storage.bucket()

cur_path = os.path.dirname(__file__)
#load data
df = pd.read_csv(f'{cur_path}/../data/data.csv')

#https://www, if we have /generate, send our data to the url
APP_ROOT = os.getenv('APP_ROOT', '/generate')


@app.route(APP_ROOT, methods=["POST"])
def generate_pastpaper():
    data = request.json
    topic_list = data.get('topics')
    options = data.get('options')  # 21, 41, 61...

    topic_df = df[df['topic'].isin(topic_list)]

    component2 = topic_df[topic_df['component'] == options[0]]
    component4 = topic_df[topic_df['component'] == options[1]]
    component6 = topic_df[topic_df['component'] == options[2]]

    
    component2_questions = []
    for i in range(1,41):
         component2_questions.append(component2[component2['question number'] == i].sample(1))

    component4_questions = []
    for i in range(1,7):
         component4_questions.append(component4[component4['question number'] == i].sample(1))
         
    component6_questions = []
    for i in range(1,5):
         component6_questions.append(component6[component6['question number'] == i].sample(1))



    # images = {
    #     'component2': component2['screenshot_path'].to_list(),
    #     'component4': component4['screenshot_path'].to_list(),
    #     'component6': component6['screenshot_path'].to_list()
    # }

    images = {
        'component2': ['screenshots/2010/march/component2/q1.png'],
        'component4': ['screenshots/2010/march/component2/q1.png'],
        'component6': ['screenshots/2010/march/component2/q1.png'],
    }

    component2_pdf = process_pdf(images['component2'], bucket, topic_list, options[0])
    component4_pdf = process_pdf(images['component4'], bucket, topic_list, options[1])
    component6_pdf = process_pdf(images['component6'], bucket, topic_list, options[2])

    pdfs = {
        'component2': component2_pdf,
        'component4': component4_pdf,
        'component6': component6_pdf,
    }

    return pdfs
