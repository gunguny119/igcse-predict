import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('igcse-predict-c18eb87031fd.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'igcse-predict.appspot.com'
})

bucket = storage.bucket()

filename = "screenshots/2010/march/component2/q1.png"

blob = bucket.blob(filename)
blob.upload_from_filename(filename)