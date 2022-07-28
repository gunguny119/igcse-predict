import os
import re
from pprint import pprint

import requests

topic_list = [
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

topic_links = {}
for t in topic_list:
    response = requests.get(
        f"https://www.physicsandmathstutor.com/chemistry-revision/igcse-cie/{t}/")
    open(f"pmt/{t}/index.html", "wb").write(response.content)

    with open(f'{t}/index.html') as f:
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
                    open(f"{t}/{os.path.basename(match)}", "wb").write(response.content)