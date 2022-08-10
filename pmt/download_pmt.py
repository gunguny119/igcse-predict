import os
import re

import requests
############################# Change Here ######################################
TOPIC_LIST = [
    "particulate-nature-of-matter",
    "experimental-techniques",
    "atoms-elements-compounds",
    "stoichiometry",
    "electricity-and-chemistry",
    "chemical-energetics",
    "chemical-reactions",
    "acids-bases-salts",
    "periodic-table",
    "metals",
    "air-and-water",
    "sulfur",
    "carbonates",
    "organic-chemistry",
]
SUBJECT = "chemistry"

#################################################################################
topic_links = {}
for t in TOPIC_LIST:
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
