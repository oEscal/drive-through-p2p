
if [[ $# -ne 1 ]]; then
   printf "usage:\n$./init.sh [number of clients]\n"
else
   for ((i=1; i < $1; i++)); do
      gnome-terminal -x bash -c "python3 client_stor.py -p $((5000 + $i)); exec bash" 2>&1 >/dev/null
      #python3 client_stor.py -p $((5000 + $i)) &
   done
fi