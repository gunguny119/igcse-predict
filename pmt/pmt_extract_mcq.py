import re
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
    data = []
    for t in topic_list:
        for qp in glob.glob(f'pastpapers/{t}/*QP.pdf.txt'):
            if not '(Multiple Choice)' in qp:
                continue

            with open(qp) as f:
                questions = segment_questions_component2(f.readlines(), 21, '0620')

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

    df.to_csv('pmt_mcq.csv', index=False)


if __name__ == '__main__':
    main()
