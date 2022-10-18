mkdir output/comp
for num in 1 2 3 4 5
do
    python3 train_test_comp.py comp/data$num 2000 3
done
