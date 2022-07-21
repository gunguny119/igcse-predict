for y in {2010..2021}; do
    for m in march summer winter; do
        for c in 2 4 6; do
            mkdir -p screenshots/$y/$m/component$c
        done
    done
done