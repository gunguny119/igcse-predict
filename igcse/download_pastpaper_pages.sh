subject=chemistry
code_id=0620
components=(2 4 6)

echo downloading...
command="sh download.sh $subject $code_id ${components[@]}"
eval $command
echo finished downloading.

echo extracting text...
command="sh pdf2txt.sh $subject $code_id ${components[@]}"
eval $command
echo finished extracting texts from pastpapers.

echo extracting 1 page screenshots...
command="python extract_pages.py --subject $subject"
eval $command
echo finished extracting 1 page screenshots.