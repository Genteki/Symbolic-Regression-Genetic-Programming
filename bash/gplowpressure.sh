mkdir output/gp_low_pressure
for num in 1 2 3 4 5
do
    python3 run.py gp_low_pressure/data$num 1000 3
done
