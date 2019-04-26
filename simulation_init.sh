if [ "$#" -ne 1 ]; then
    printf "usage:\n$./simulation_init.sh <interval in seconds>\n"

else

    declare -a nodes=("chef_init.py" "clerk_init.py" "restaurant_init.py" "waiter_init.py")
    pkill -9 python
    nodes_s=( $(echo "$(shuf -e "${nodes[@]}")" | sed -r 's/(.[^;]*;)/ \1 /g' | tr " " "\n" | shuf | tr -d " " ) )
    for i in "${nodes_s[@]}"
    do
        echo "$i"
        gnome-terminal -x bash -c "echo $i; python3 $i; exec bash" 2>&1 >/dev/null
        sleep $1
    done
fi


