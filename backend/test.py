import requests
from pprint import pprint

response = requests.post("http://127.0.0.1:5000/generate",
                         json={
                             "topics": [
                                 "1 The particulate nature of matter",
                                 "2 Experimental techniques",
                                 "3 Atoms, elements and compounds",
                             ],
                             "options": [22, 42, 62],
                         })
pprint(response.json())