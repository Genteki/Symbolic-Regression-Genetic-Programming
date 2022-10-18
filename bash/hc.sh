mkdir output/hc
for num in 1 2 3 4 5
do
    python3 run.py hc/data$num 1000 1
done
