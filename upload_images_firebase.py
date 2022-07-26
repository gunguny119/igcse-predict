import os
from re import L

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('igcse-predict-c18eb87031fd.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'igcse-predict.appspot.com'})

bucket = storage.bucket()

filename = "screenshots/2010/march/component2/q1.png"

for year in range(2016, 2022):
    for month in ['march', 'summer', 'winter']:
        for comp in os.listdir(f'screenshots/{year}/{month}'):
            if not os.path.isdir(f'screenshots/{year}/{month}/{comp}'):
                continue
            for question in os.listdir(f'screenshots/{year}/{month}/{comp}'):
                filename = f'screenshots/{year}/{month}/{comp}/{question}'
                blob = bucket.blob(filename)
                blob.upload_from_filename(filename)