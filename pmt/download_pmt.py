import os
import re

import requests
############################# Change Here ######################################
TOPIC_LIST = [
    "characteristics-and-classification-of-living-organisms",
    "organisation-of-organism",
    "movement-in-out-of-cells",
    "biological-molecules",
    "enzymes",
    "plant-nutrition",
    "human-nutrition",
    "transport-in-plants"
    "transport-in-animals",
    "diseases-and-immunity",
    "gas-exchange-in-humans",
    "respiration",
    "excretion-in-humans",
    "coordination-and-response",
    "drugs",
    "reproduction",
    "inheritance",
    "variation-and-selection",
    "organisms-and-their-environment",
    "biotechnology-and-genetic-engineering",
    "human-influences-on-ecosystems",
]
SUBJECT = "biology"

#################################################################################
topic_links = {}
for t in TOPIC_LIST:
    os.makedirs(f'pastpapers/{SUBJECT}/{t}', exist_ok=True)
    response = requests.get(
        f"https://www.physicsandmathstutor.com/{SUBJECT}-revision/igcse-cie/{t}/")
    open(f"pastpapers/{SUBJECT}/{t}/index.html", "wb").write(response.content)

    with open(f'pastpapers/{SUBJECT}/{t}/index.html') as f:
        found = False
        finished = False
        links = []
        for line in f:
            if '<h4><a id="questions"></a>Questions by Topic:</h4>' in line:
                found = True
                finished = False
                continue

            if '<span class="cp-load-after-post"></span> </div>' in line:
                finished = True

            if found and not finished:
                matches = re.findall(r"<a href=\"(.*?)\">", line)
                for match in matches:
                    if not match.endswith('.pdf'):
                        continue
                    response = requests.get(match)
                    open(f"pastpapers/{SUBJECT}/{t}/{os.path.basename(match)}",
                         "wb").write(response.content)
