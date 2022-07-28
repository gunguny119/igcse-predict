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
    data = []
    for t in topic_list:
        for qp in glob.glob(f'pmt/{t}/*QP.pdf.txt'):
            if '(Multiple Choice)' in qp:
                continue

            with open(qp) as f:
                print(qp)
                questions, _ = segment_questions_component46(f.readlines(), 41, '0620')

            question_numbers = list(range(1, len(questions) + 1))
            curr_data = {
                'component': [4] * len(questions),
                'question number': question_numbers,
                'text': questions,
                'topic': [t] * len(questions),
            }
            data.append(pd.DataFrame(curr_data))

    df = pd.concat(data)
    df.sort_values(by=['topic'], inplace=True)

    df.to_csv('pmt_long_answers.csv', index=False)


if __name__ == '__main__':
    main()
