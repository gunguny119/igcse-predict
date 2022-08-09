import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subject', type=str, default='chemistry')
args = parser.parse_args()

with open(f'{args.subject}/pmt_mcq.csv') as f:
    mcq = f.readlines()

with open(f'{args.subject}/pmt_long_answers.csv') as f:
    la = f.readlines()

la.pop(0)

data = mcq + la

with open(f'{args.subject}/pmt_train.csv', 'w') as f:
    f.writelines(data)