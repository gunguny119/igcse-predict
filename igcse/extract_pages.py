import argparse
import os
from pdf2image import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument('--subject', type=str, default='chemistry')
parser.add_argument('--ms', action='store_true')
args = parser.parse_args()

save_path = '../marking_schemes' if args.ms else '../screenshots'
if args.subject != 'chemistry':
    save_path = f'{save_path}/{args.subject}'

os.makedirs(save_path, exist_ok=True)

month_map = {'m': 'march', 's': 'summer', 'w': 'winter'}

for year in range(2016, 2022):
    folder = 'ms' if args.ms else 'qp'
    for f in os.listdir(f'pastpapers/{args.subject}/{year}/{folder}/'):
        fname = f'pastpapers/{args.subject}/{year}/{folder}/{f}'

        _, month, _, comp = f.split('_')
        month = month_map[month[0]]
        comp = comp.replace('.pdf', '')

        image_dir = f'{save_path}/{year}/{month}/component{comp}'
        os.makedirs(image_dir, exist_ok=True)

        pages = convert_from_path(fname)

        for i, page in enumerate(pages):
            page.save(f'{image_dir}/page' + str(i) + '.png', 'PNG')
