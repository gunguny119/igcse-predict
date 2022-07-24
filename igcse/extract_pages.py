import os
from pdf2image import convert_from_path

save_path = '../screenshots'
os.makedirs(save_path, exist_ok=True)

month_map = {'m': 'march', 's': 'summer', 'w': 'winter'}

for year in range(2016, 2022):
    for f in os.listdir(f'pastpapers/{year}/qp/'):
        fname = f'pastpapers/{year}/qp/{f}'

        _, month, _, comp = f.split('_')
        month = month_map[month[0]]
        comp = comp.replace('.pdf', '')

        image_dir = f'{save_path}/{year}/{month}/component{comp}'
        os.makedirs(image_dir, exist_ok=True)

        pages = convert_from_path(fname)

        for i, page in enumerate(pages):
            page.save(f'{image_dir}/page' + str(i) + '.png', 'PNG')
