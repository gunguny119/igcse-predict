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
    "characteristics-and-classification-of-living-organisms":"1. Characteristics and Classification of Living Organisms & 2. Organisation of the Organism",
    "organisation-of-organism": "1. Characteristics and Classification of Living Organisms & 2. Organisation of the Organism",
    "movement-in-out-of-cells": "3. Movement in and out of Cells",
    "biological-molecules": "4. Biological Molecules",
    "enzymes" : "5. Enzymes",
    "plant-nutrition": "6. Plant Nutrition & 7. Human Nutrition",
    "human-nutrition" : "6. Plant Nutrition & 7. Human Nutrition",
    "transport-in-plants":"8. Transport in Plants & 9. Transport in Animals",
    "transport-in-animals":"8. Transport in Plants & 9. Transport in Animals",
    "diseases-and-immunity":"10. Diseases and Immunity",
    "gas-exchange-in-humans": "11. Gas Exchange in Humans & 12. Respiration",
    "respiration":"11. Gas Exchange in Humans & 12. Respiration",
    "excretion-in-humans":"13. Excretion in Humans",
    "coordination-and-response": "14. Coordination and Response",
    "drugs" : "15. Drugs",
    "reproduction" : "16. Reproduction & 17. Inheritance & 18. Variation and Selection",
    "inheritance" : "16. Reproduction & 17. Inheritance & 18. Variation and Selection",
    "variation-and-selection": "16. Reproduction & 17. Inheritance & 18. Variation and Selection",
    "organisms-and-their-environment": "19. Organisms and their Environment",
    "biotechnology-and-genetic-engineering":"20. Biotechnology and Genetic Engineering",
    "human-influences-on-ecosystems":"21. Human Influences on Ecosystems",
}


def segment_questions_component2(lines, component, subject):
    q_found = False
    answer_found = [False, False, False, False]

    questions = []
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
            if len(current_segment) > 0:
                questions.append(' '.join(current_segment))
            break

        if re.match('\d+\s+', line):
            if not q_found:
                # first question
                q_found = True
                current_segment.append(line)
                continue
            if all(answer_found):
                q_found = True
                if len(current_segment) > 0:
                    questions.append(' '.join(current_segment))
                    current_segment = []
                    answer_found = [False, False, False, False]

        for i, x in enumerate('ABCD'):
            if line.startswith(x):
                answer_found[i] = True

        if q_found:
            current_segment.append(line)

    return questions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, default='chemistry')
    parser.add_argument('--code', type=str, default='0620')
    args = parser.parse_args()
    data = []
    for t in topic_list:
        for qp in glob.glob(f'pastpapers/{args.subject}/{t}/*QP.pdf.txt'):
            if not '(Multiple Choice)' in qp:
                continue

            with open(qp) as f:
                questions = segment_questions_component2(f.readlines(), 21, args.code)

            # questions = list(filter(lambda x: re.match(r'\d+\s+', x), questions))

            question_numbers = [int(re.split(r'\s+', q)[0]) for q in questions]
            data.append(
                pd.DataFrame({
                    'component': [21] * len(questions),
                    'question number': question_numbers,
                    'text': questions,
                    'topic': [topic_map[t]] * len(questions),
                }))

    df = pd.concat(data)
    df.sort_values(by=['topic'], inplace=True)

    os.makedirs(args.subject, exist_ok=True)
    df.to_csv(f'{args.subject}/pmt_mcq.csv', index=False)


if __name__ == '__main__':
    main()
