subject=$1
code_id=$2
components=($3 $4 $5)
seasons=(m s w)
alts=(1 2 3)

 for i in {16..21}; do
    for season in ${seasons[@]}; do
        for component in ${components[@]}; do
            for alt in ${alts[@]}; do
                if [[ -f pastpapers/${subject}/20${i}/qp/${code_id}_${season}${i}_qp_${component}${alt}.pdf ]]; then
                    pdf2txt.py -o pastpapers/${subject}/20${i}/${code_id}_${season}${i}_qp_${component}${alt}.txt pastpapers/${subject}/20${i}/qp/${code_id}_${season}${i}_qp_${component}${alt}.pdf
                fi
            done
        done
    done
done