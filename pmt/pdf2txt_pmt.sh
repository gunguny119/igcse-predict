
for d in "pmt/*"; do
    for f in "$d/*QP.pdf"; do
        # echo $f
        for fname in $f; do
            command="pdf2txt.py -o \"$fname.txt\" \"$fname\""
            eval $command
        done
    done
done