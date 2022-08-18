# IGCSE - Predict

This project generates chemistry past paper.

# How to Add New Topic?

## Collect IGCSE data

### 0. Check environment

1. Run the following in a terminal, not a vs-code terminal.
2. use `tf-m1` conda environment.

    ```
    conda activate tf-m1
    ```

3. install packages:

    ```
    pip install pdfminer
    pip install pdf2image
    brew install wget
    brew install poppler
    ```

4. go to `igcse-predict` directory

    ```
    cd path/to/igcse-predict
    ```

### 1. Download & Extract Text and Pages

1. open `igcse/download_pastpaper_pages.sh` and change the subject name, code, and components.
2. type the following commands to the terminal:

```
cd igcse
sh download_pastpaper_pages.sh
```

### 2. Extract Questions from Text

The SUBJECT and CODE should change according to your interested subject.
For COMP, put the component number that contains mcq questions.
```
python igcse_extract_la.py --subject SUBJECT --code CODE --mcq_component COMP
python igcse_extract_mcq.py --subject SUBJECT --code CODE --mcq_component COMP
```
you will get `[SUBJECT]_mcq_2016-2021.csv`, `[SUBJECT]_la_2016-2021.csv`.

### 3. Collect MCQ answers

Manually collect MCQ answers from marking schemes from 2016 to 2021 (or other years).

save it as `[SUBJECT]_mcq_ms_2016-2021.csv`.

For reference, take a look at `chemistry_mcq_ms_20216-2021.csv`.

### 4. merge components

1. Run:
   ```
   python merge_components.py --subject SUBJECT --start_year 2016 --end_year 2021
   ```
2. You will end up with `[SUBJECT]_all_2016-2021.csv`

## Collect Train data

### Collect PMT data

1. Open `download_pmt.py` and edit `TOPIC_LIST` and the `SUBJECT`.
2. Then:
    ```
    python download_pmt.py
    sh pdf2txt_pmt.sh
    ```
3. open `pmt_extract_la.py` and `pmt_extract_mcq.py` and edit the `topic_list` and `topic_map`. Then:
   ```
   python pmt_extract_la.py --subject SUBJECT --code CODE
   python pmt_extract_mcq.py --subject SUBJECT --code CODE
   ```

4. Then, run the following:
    ```
    python pmt_merge.py --subject SUBJECT
    ```


## Train Model

1. open BertTrain.ipynb in google colab (using github or upload)
2. upload `pmt_train.csv`.
3. edit `topics` list.
4. Update `out_dim` and `subject`.
5. Run all cells.
6. model will be saved at google drive `models/` foler.

## Create Database
1. open inference.ipynb in google colab.
2. edit the cell under `Run` accordingly (esp. topic_list, subject, data_path, model_path).
3. upload your data file (`[subject]_all_2016-2021.csv`)
4. run all cells.
5. download `all_data_labeled.csv`
6. change the name of the csv file to `[subject]_data.csv`
7. move this file under `igcse-backend/data/`


## Deploy Backend

1. go to igcse-backend folder (in terminal or vs-code)
2. git push.
3. go to [render](https://dashboard.render.com).
4. manual deploy option - deploy last commit.


## FAQ
1. What to do if I mistakenly deleted some screenshots?
    ```
    cd igcse
    python extract_pages.py --subject SUBJEECT
    ```

    if you need screenshots for marking schemes,
    ```
    python extract_pages.py --subject SUBJEECT --ms
    ```