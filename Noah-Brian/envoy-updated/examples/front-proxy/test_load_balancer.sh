#!/bin/bash

declare -A dict

for((x=0; x < 100; x++))
do
    result=$(redis-cli -h localhost -p 8080 get server)
    ((++dict[$result]))
done

for key in "${!dict[@]}";
do
    echo "Server $key was hit ${dict[$key]} times"
done

echo "All done"