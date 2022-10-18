mkdir output/random_search
for num in 1 2 3 4 5
do
    python random_search.py random_search/data$num 200
done
