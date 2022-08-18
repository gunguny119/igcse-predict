import argparse
import re
import os
import pandas as pd
import glob

topic_list = [
    "characteristics-and-classification-of-living-organisms",
    "organisation-of-organism",
    "movement-in-out-of-cells",
    "biological-molecules",
    "enzymes",
    "plant-nutrition",
    "human-nutrition",
    "transport-in-plants",
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

topic_map = {
    "characteristics-and-classification-of-living-organisms":"1. Characteristics and Classification of Living Organisms",
    "organisation-of-organism": "2. Organisation of the Organism",
    "movement-in-out-of-cells": "3. Movement in and out of Cells",
    "biological-molecules": "4. Biological Molecules",
    "enzymes" : "5. Enzymes",
    "plant-nutrition": "6. Plant Nutrition",
    "human-nutrition" : "7. Human Nutrition",
    "transport-in-plants":"8. Transport in Plants",
    "transport-in-animals":"9. Transport in Animals",
    "diseases-and-immunity":"10. Diseases and Immunity",
    "gas-exchange-in-humans": "11. Gas Exchange in Humans",
    "respiration":"12. Respiration",
    "excretion-in-humans":"13. Excretion in Humans",
    "coordination-and-response": "14. Coordination and Response",
    "drugs" : "15. Drugs",
    "reproduction" : "16. Reproduction",
    "inheritance" : "17. Inheritance",
    "variation-and-selection": "18. Variation and Selection",
    "organisms-and-their-environment": "19. Organisms and their Environment",
    "biotechnology-and-genetic-engineering":"20. Biotechnology and Genetic Engineering",
    "human-influences-on-ecosystems":"21. Human Influences on Ecosystems",
}
def segment_questions_component46(lines, component, subject):
    questions = []
    marks = []
    current_segment = []
    for line in lines:
        line = line.strip()
        line = re.sub('[\x13\x17]', '', line)
        if len(line) == 0:
            continue
        if line.startswith('©') or '[Turn Over' in line or line.startswith(
                f'{subject}/{component}'):
            continue
        if 'BLANK PAGE' in line:
            break

        if '[Total:' in line:
            questions.append(re.sub('\t', ' ', ' '.join(current_segment)))
            current_segment = []
            marks.append(int(re.search(r'[\[\(]Total:\s*(\d+?)[\]\)]', line).group(1)))
            continue

        current_segment.append(line)

    return questions, marks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, default='chemistry')
    parser.add_argument('--code', type=str, default='0620')
    args = parser.parse_args()
    data = []
    for t in topic_list:
        for qp in glob.glob(f'pastpapers/{args.subject}/{t}/*QP.pdf.txt'):
            if '(Multiple Choice)' in qp:
                continue

            with open(qp) as f:
                print(qp)
                questions, _ = segment_questions_component46(f.readlines(), 41, args.code)

            question_numbers = list(range(1, len(questions) + 1))
            curr_data = {
                'component': [4] * len(questions),
                'question number': question_numbers,
                'text': questions,
                'topic': [topic_map[t]] * len(questions),
            }
            data.append(pd.DataFrame(curr_data))

    df = pd.concat(data)
    df.sort_values(by=['topic'], inplace=True)

    os.makedirs(args.subject, exist_ok=True)
    df.to_csv(f'{args.subject}/pmt_long_answers.csv', index=False)


if __name__ == '__main__':
    main()
