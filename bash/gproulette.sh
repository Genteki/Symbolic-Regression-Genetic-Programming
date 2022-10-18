mkdir output/gp_roulette
for num in 1 2 3 4 5
do
    python3 test_roulette.py gp_roulette/data$num 1000 2
done
