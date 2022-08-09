import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--subject', type=str, default='chemistry')
parser.add_argument('--start_year', type=str, default='2016')
parser.add_argument('--end_year', type=str, default='2021')
args = parser.parse_args()

qp_mcq = pd.read_csv(f'{args.subject}_mcq_{args.start_year}-{args.end_year}.csv')
mcq_ms = pd.read_csv(f'{args.subject}_mcq_ms_{args.start_year}-{args.end_year}.csv')
qp_la = pd.read_csv(f'{args.subject}_la_{args.start_year}-{args.end_year}.csv')

processed_qp_mcq = qp_mcq[qp_mcq['text'].apply(lambda x: x.count('?')) == 1]

df = pd.merge(mcq_ms,
              processed_qp_mcq,
              how='outer',
              on=['year', 'month', 'component', 'question number'])

all_df = pd.concat([df, qp_la], ignore_index=True)

all_df.to_csv(f'{args.subject}_all_{args.start_year}-{args.end_year}.csv', index=False)

################################################################################
# THIS PART is to merge hand-labeled data with automatic data.
# Comment out only if you need this part (e.g. chemistry)
################################################################################
# all_df = pd.read_csv(f'all_{args.start_year}-{args.end_year}.csv')
# labeled = pd.read_csv(f'component24_2020-{args.end_year}_labeled.csv')

# df = pd.merge(all_df,
#               labeled,
#               how='outer',
#               on=['year', 'month', 'component', 'question number'])

# df['text'] = df[['text_x', 'text_y']].apply(lambda x: x['text_x']
#                                             if pd.isna(x['text_y']) else x['text_y'],
#                                             axis=1)
# df.drop(columns=['text_x', 'text_y'], inplace=True)

# df.to_csv('all_data.csv', index=False)
