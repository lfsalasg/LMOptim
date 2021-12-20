#!/bin/bash

i=0
module=$1
script=$2
tasks=$3
cores=$4
start_time=$(date +%s)
while [ $i -le $tasks ]
do
    for j in $(seq 0 $cores)
    do
        if [ $i -gt $tasks ]
        then
            break
        fi
        echo "On CPU $j Task $i"
        taskset --cpu-list $j $module $script &
        i=$(($i+1))
    done
    wait
done

wait
end_time=$(date +%s)
echo "Finalizó"
elapsed=$(( end_time - start_time ))

echo $elapsed