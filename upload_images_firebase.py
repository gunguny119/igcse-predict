import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('backend/igcse-predict-c18eb87031fd.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'igcse-predict.appspot.com'})

bucket = storage.bucket()

ms = False  # if true, upload marking scheme
subject = 'chemistry'

if ms:
    folder = 'marking_schemes'
else:
    folder = 'screenshots'

if subject != 'chemistry':
    folder = f'{folder}/{subject}'

for year in range(2016, 2022):
    for month in ['march', 'summer', 'winter']:
        for comp in os.listdir(f'{folder}/{year}/{month}'):
            if not os.path.isdir(f'{folder}/{year}/{month}/{comp}'):
                continue
            for question in os.listdir(f'{folder}/{year}/{month}/{comp}'):
                # m1_1.png  -> q1_p1.png
                # q1.png -> q1_p1.png
                # renamed_question = question.replace('m', 'q')
                # renamed_question = renamed_question.replace('_ppp', '_p')
                # if not '_' in question:
                #     renamed_question = renamed_question.split('.')[0] + '_p1.png'

                filename = f'{folder}/{year}/{month}/{comp}/{question}'
                # renamed_filename = f'{folder}/{year}/{month}/{comp}/{renamed_question}'
                if question.startswith('page'):
                    continue

                # os.rename(filename, renamed_filename)
                # continue

                blob = bucket.blob(filename)
                if blob.exists():
                    continue
                blob.upload_from_filename(filename)