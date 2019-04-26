nodes=("Chef.py" "Clerk.py" "Restaurant.py" "Waiter.py")

if [[ ${#} -ne 2 ]]; then
   echo -e "Error\nUsage: ./switch_to_v2.sh <import file to substitute> <import file to add>"
else
   for i in "${nodes[@]}"; do
      echo "Modified:" $i
      content=$(cat $i)

      new_content=${content//"from $1 import RingNode"/"from $2 import RingNode"}

      printf "%s" "$new_content" > $i
   done
fi