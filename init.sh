
if [[ $# -ne 1 ]]; then
   printf "usage:\n$./init.sh [number of clients]\n"
else
   for ((i=1; i < $1; i++)); do
      python3 client.py -p $((5000 + $i)) &
   done
fi