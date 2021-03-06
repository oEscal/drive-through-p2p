if [ "$#" -ne 2 ]; then
    printf "usage:\n$./simulation_v2_init.sh.sh <Number of iterations> <Time between process kills ( in seconds ) >\n"

else
    declare -a nodes=("chef_init.py" "clerk_init.py" "restaurant_init.py" "waiter_init.py")
    nodes_s=( $(echo "$(shuf -e "${nodes[@]}")" | sed -r 's/(.[^;]*;)/ \1 /g' | tr " " "\n" | shuf | tr -d " " ) )
    for i in "${nodes_s[@]}"
    do
        echo "$i initialized"
        gnome-terminal -x bash -c "echo $i; python3 $i; exec bash" 2>&1 >/dev/null
    done
    for ((i=0; i < $1; i++));
    do
        index=$(( ( RANDOM % 4 ) )) 
        program=${nodes_s[$index]}
        printf "\n$program being killed\n"
        IFS='.' read -ra ADDR <<< "$program"
        pkill -f $ADDR
        sleep $2
        gnome-terminal -x bash -c "echo $program; python3 $program; exec bash" 2>&1 >/dev/null
    done
fi