
if [[ $# -ne 2 ]]; then
   printf "usage:\n$./init.sh [script to run] [number of clients]\n"
else
   for ((i=1; i < (( $2 + 1 )); i++)); do
      gnome-terminal -x bash -c "python3 $1 -p $((5000 + $i)); exec bash" 2>&1 >/dev/null
   done
fi