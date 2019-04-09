screen=2200

alias k='killall xterm'

#xterm -geometry 73x31+$((2500 - $screen))+100 -T "client" -e python3 client.py 10 &
xterm -hold -geometry 73x31+$((3000 - $screen))+100 -T "restaurant" -hold -e python3 restaurant.py &
xterm -geometry 73x31+$((2500 - $screen))+700 -T "chef" -hold -e python3 chef.py &
xterm -geometry 73x31+$((3000 - $screen))+700 -T "receptionist" -hold -e python3 receptionist.py &
xterm -geometry 73x31+$((3500 - $screen))+400 -T "clerk" -hold -e python3 clerk.py &
