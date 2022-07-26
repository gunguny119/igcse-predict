import argparse
import os
import re
import pandas as pd


def segment_questions_la(lines, component, subject):
    question_found = False
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
        if 'This document' in line:
            question_found = True
            continue

        if '[Total:' in line:
            # start = 0
            # for i, x in enumerate(current_segment):
            #     if re.match(r'^\d+.*', x):
            #         start = i
            #         break
            # current_segment = current_segment[start:]
            questions.append(re.sub('\t', ' ', ' '.join(current_segment)))
            current_segment = []
            marks.append(int(re.search(r'\[Total:\s(\d+?)\]', line).group(1)))
            continue

        if question_found:
            current_segment.append(line)

    return questions, marks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, default='physics')
    parser.add_argument('--code', type=str, default='0625')
    parser.add_argument('--mcq_component', type=str, default='2')
    args = parser.parse_args()

    if args.subject == 'chemistry':
        screenshot_dir = 'screenshots'
        ms_dir = 'marking_schemes'
    else:
        screenshot_dir = f'screenshots/{args.subject}'
        ms_dir = f'marking_schemes/{args.subject}'

    month_map = {'m': 'march', 's': 'summer', 'w': 'winter'}
    data = []
    for year in range(2016, 2022):
        for qp in os.listdir(f'pastpapers/{args.subject}/{year}'):
            if not qp.endswith('txt'):
                continue
            if f'qp_{args.mcq_component}' in qp:
                continue
            fname = f'pastpapers/{args.subject}/{year}/{qp}'

            names = qp.replace('.txt', '')
            _, month, _, component = names.split('_')

            with open(fname) as f:
                questions, marks = segment_questions_la(f.readlines(), component,
                                                        args.code)

            # questions = list(filter(lambda x: re.match(r'^\d+.*', x), questions))
            # question_numbers = [int(re.split(r'\s', q)[0]) for q in questions]
            question_numbers = list(range(1, len(questions) + 1))
            screenshot_paths = [
                f'{screenshot_dir}/{year}/{month_map[month[0]]}/component{component}/q{n}'
                for n in question_numbers
            ]
            ms_paths = [
                f'{ms_dir}/{year}/{month_map[month[0]]}/component{component}/q{n}'
                for n in question_numbers
            ]
            curr_data = {
                'year': [year] * len(questions),
                'month': [month[0]] * len(questions),
                'component': [component] * len(questions),
                'question number': question_numbers,
                'text': questions,
                'screenshot_path': screenshot_paths,
                'ms_path': ms_paths,
                'marks': marks,
            }
            data.append(pd.DataFrame(curr_data))

    df = pd.concat(data)
    df.sort_values(by=['year', 'month', 'component', 'question number'], inplace=True)

    df.to_csv(f'{args.subject}_la_2016-2021.csv', index=False)


if __name__ == '__main__':
    main()
