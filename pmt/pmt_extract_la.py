import argparse
import re
import os
import pandas as pd
import glob

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

topic_map = {
    "particulate-nature-of-matter": "1 The particulate nature of matter",
    "experimental-techniques": "2 Experimental techniques",
    "atoms-elements-compounds": "3 Atoms, elements and compounds",
    "stoichiometry": "4 Stoichiometry",
    "electricity-and-chemistry": "5 Electricity and chemistry",
    "chemical-energetics": "6 Chemical energetics",
    "chemical-reactions": "7 Chemical reactions",
    "acids-bases-salts": "8 Acids, bases and salts",
    "periodic-table": "9 The Periodic Table",
    "metals": "10 Metals",
    "air-and-water": "11 Air and water",
    "sulfur": "12 Sulfur",
    "carbonates": "13 Carbonates",
    "organic-chemistry": "14 Organic chemistry",
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
