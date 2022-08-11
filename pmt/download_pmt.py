import os
import re

import requests
############################# Change Here ######################################
TOPIC_LIST = [
    "general-physics",
    "thermal-physics",
    "properties-of-waves-light-sound",
    "electricity-and-magnetism",
    "atomic-physics",

]
SUBJECT = "physics"

#################################################################################
topic_links = {}
for t in TOPIC_LIST:
    os.makedirs(f'{SUBJECT}/{t}', exist_ok=True)
    response = requests.get(
        f"https://www.physicsandmathstutor.com/{SUBJECT}-revision/igcse-cie/{t}/")
    open(f"{SUBJECT}/{t}/index.html", "wb").write(response.content)

    with open(f'{SUBJECT}/{t}/index.html') as f:
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
                    open(f"{SUBJECT}/{t}/{os.path.basename(match)}",
                         "wb").write(response.content)
