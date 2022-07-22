import os
import re
import pandas as pd


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

        if re.match('\d+  ', line):
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
    month_map = {'m': 'march', 's': 'summer', 'w': 'winter'}
    data = []
    for year in range(2016, 2022):
        for qp in os.listdir(str(year)):
            if not qp.endswith('txt'):
                continue
            if not 'qp_2' in qp:
                continue
            fname = f'{year}/{qp}'

            names = qp.replace('.txt', '')
            _, month, _, component = names.split('_')

            with open(fname) as f:
                questions = segment_questions_component2(f.readlines(), component, '0620')

            questions = list(filter(lambda x: re.match(r'\d+  ', x), questions))

            question_numbers = [int(q.split(' ')[0]) for q in questions]
            screenshot_paths = [
                f'{year}/{month_map[month[0]]}/component{component[0]}/q{n}.png'
                for n in question_numbers
            ]
            data.append(
                pd.DataFrame({
                    'year': [year] * len(questions),
                    'month': [month[0]] * len(questions),
                    'component': [component] * len(questions),
                    'question number': question_numbers,
                    'text': questions,
                    'screenshot_path': screenshot_paths,
                }))

    df = pd.concat(data)

    df.to_csv('component2_2016-2021.csv', index=False)


if __name__ == '__main__':
    main()
