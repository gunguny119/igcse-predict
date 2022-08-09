subject=chemistry
code_id=0620
seasons=(m s w)
components=(2 4 6)
alts=(1 2 3)

 mkdir -P pastpapers/${subject}
 for i in {16..21}; do
    mkdir pastpapers/${subject}/20${i}
    for season in ${seasons[@]}; do
        for type in ms qp; do
            mkdir pastpapers/${subject}/20${i}/$type
            for component in ${components[@]}; do
                for alt in ${alts[@]}; do
                    wget https://papers.gceguide.com/Cambridge%20IGCSE/$subject%20\(${code_id}\)/20$i/${code_id}_${season}${i}_${type}_${component}${alt}.pdf -P pastpapers/${subject}/20${i}/$type
                done
            done
        done
    done
done