mkdir output/gp_tournmant
for num in 1 2 3 4 5
do
    python3 run.py gp_tournmant/data$num 1000 2
done
