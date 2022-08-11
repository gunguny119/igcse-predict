import argparse
import os
import re
import pandas as pd


def segment_questions_mcq(lines, component, subject):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, default='physics')
    parser.add_argument('--code', type=str, default='0625')
    parser.add_argument('--mcq_component', type=str, default='2')
    args = parser.parse_args()

    if args.subject == 'physics':
        screenshot_dir = 'screenshots'
    else:
        screenshot_dir = f'screenshots/{args.subject}'

    month_map = {'m': 'march', 's': 'summer', 'w': 'winter'}
    data = []
    for year in range(2016, 2022):
        for qp in os.listdir(f'pastpapers/{args.subject}/{year}'):
            if not qp.endswith('txt'):
                continue
            if not f'qp_{args.mcq_component}' in qp:
                continue
            fname = f'pastpapers/{args.subject}/{year}/{qp}'

            names = qp.replace('.txt', '')
            _, month, _, component = names.split('_')

            with open(fname) as f:
                questions = segment_questions_mcq(f.readlines(), component, args.code)

            questions = list(filter(lambda x: re.match(r'\d+  ', x), questions))

            question_numbers = [int(q.split(' ')[0]) for q in questions]
            screenshot_paths = [
                f'{screenshot_dir}/{year}/{month_map[month[0]]}/component{component}/q{n}'
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
    df.sort_values(by=['year', 'month', 'component', 'question number'], inplace=True)

    df.to_csv(f'{args.subject}_mcq_2016-2021.csv', index=False)


if __name__ == '__main__':
    main()
