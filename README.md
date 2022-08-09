# IGCSE - Predict

This project generates chemistry past paper.

# How to Add New Topic?

## Collect IGCSE data
### 1. Download Pastpapers

1. open `igcse/download.sh` and change the topic name and the code.
2. Change the components or alts in the code accordingly.
3. type the following commands to the terminal:

```
cd igcse
sh download.sh
```

### 2. Extract Text from PDF

change the code name in `pdf2txt.sh`
```
sh pdf2txt.sh
```

### 3. Extract pages, long answers and mcqs

```
python extract_pages.py
python igcse_extract_la.py
python igcse_extract_mcq.py
```

### 4. merge components

1. open `merge_components.ipynb`
2. change the file names to reflect your current subject .csv.
3. Run all cells until `Merge with labeled data`
4. You will end up with `[subject]_all_2016-2021.csv`

## Collect Train data

### Collect PMT data

1. Open `download_pmt.py` and edit `topic_list` and the subject name in the link.
2. open `pmt_extract_la.py` and `pmt_extract_mcq.py` and edit the `topic_list` and `topic_map`.
```
python download_pmt.py
sh pdf2txt_pmt.sh
python pmt_extract_la.py
python pmt_extract_mcq.py
```

1. open `pmt_mcq.csv`.
2. copy all lines except for the first line.
3. open `pmt_long_answers.csv`.
4. paste and save.
5. rename `pmt_long_answers.csv` to `pmt_train.csv`.

## Train Model

1. open BertTrain.ipynb in google colab (using github or upload)
2. upload `pmt_train.csv`.
3. edit `topics` list.
4. Run all cells.
5. model will be saved at google drive `models/` foler.

## Create Database
1. open inference.ipynb in google colab.
2. edit the cell under `Run` accordingly.
3. upload your data file (`[subject]_all_2016-2021.csv`)
4. run all cells.
5. download `all_data_labeled.csv`
6. change the name of the csv file to `[subject]_data.csv`
7. move this file under `igcse-backend/data/`


## Deploy Backend

1. go to igcse-backend folder (in terminal or vs-code)
2. git push.
3. go to dashboard.render.com.
4. manual deploy option - deploy last commit.