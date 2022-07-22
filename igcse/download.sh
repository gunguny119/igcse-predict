 mkdir pastpapers
 for i in {10..21}; do
    mkdir 20${i}
    for season in m s w; do
        for type in ms qp; do
            mkdir 20${i}/$type
            for component in 2 4 6; do
                for alt in 1 2 3; do
                    wget https://papers.gceguide.com/Cambridge%20IGCSE/Chemistry%20\(0620\)/20$i/0620_${season}${i}_${type}_${component}${alt}.pdf -P 20${i}/$type
                done
            done
        done
    done
done