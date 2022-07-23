 for i in {10..21}; do
    for season in m s w; do
        for component in 2 4 6; do
            for alt in 1 2 3; do
                if [[ -f pastpapers/20${i}/qp/0620_${season}${i}_qp_${component}${alt}.pdf ]]; then
                    pdf2txt.py -o pastpapers/20${i}/0620_${season}${i}_qp_${component}${alt}.txt pastpapers/20${i}/qp/0620_${season}${i}_qp_${component}${alt}.pdf
                fi
            done
        done
    done
done