import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subject', type=str, default='chemistry')
args = parser.parse_args()

with open(f'{args.subject}/pmt_mcq.csv') as f:
    mcq = f.readlines()
    filtered_mcq = []
    for line in mcq:
        filtered_mcq.append(line.replace('PhysicsAndMathsTutor.com', ''))

with open(f'{args.subject}/pmt_long_answers.csv') as f:
    la = f.readlines()
    filtered_la = []
    for line in la:
        filtered_la.append(line.replace('PhysicsAndMathsTutor.com', ''))

filtered_la.pop(0)

data = filtered_mcq + filtered_la

with open(f'{args.subject}/pmt_train.csv', 'w') as f:
    f.writelines(data)