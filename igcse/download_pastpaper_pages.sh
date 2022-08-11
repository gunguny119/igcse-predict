subject=Physics
code_id=0625
components=(2 4 6)

echo downloading...
command="sh download.sh $subject $code_id ${components[@]}"
eval $command
echo finished downloading.

echo extracting text...
command="sh pdf2txt.sh $subject $code_id ${components[@]}"
eval $command
echo finished extracting texts from pastpapers.

echo "extracting 1 page screenshots for question papers..."
command="python extract_pages.py --subject $subject"
eval $command
echo finished extracting 1 page screenshots.

echo "extracting 1 page screenshots for marking schemes..."
command="python extract_pages.py --subject $subject --ms"
eval $command
echo finished extracting 1 page screenshots.