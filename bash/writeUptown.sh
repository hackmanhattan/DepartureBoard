#!/bin/bash

APIKEY="7dPziNcZAO7I14bR1o5hD1RcW3trloOo1rgN0Vhu" # SECRET! haha jk

numExample="00" # Stupid haha funny
tput civis # make cursor not be there
pad_with_zeros() { # Also stupid
   printf "%0*d\n" $1 $2
}

# Colors
NC='\033[0m' # No Color
ORANGE='\033[0;33m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'

dataUptown=(
	"MESSAGE:Uptown, The Bronx, & Upper Queens:"
	"B:34 Herald Sq.:D17N:145 St:$ORANGE"
	"D:34 Herald Sq.:D17N:Norwood-205 St:$ORANGE"
	"F:34 Herald Sq.:D17N:Jamaica-179 St:$ORANGE"
	"M:34 Herald Sq.:D17N:57 St:$ORANGE"
	"N:34 Herald Sq.:R17N:Astoria-Ditmards Blvd:$YELLOW"
	"Q:34 Herald Sq.:R17N:96 St:$YELLOW"
	"R:34 Herald Sq.:R17N:Forest Hills-71 Av:$YELLOW"
	"W:34 Herald Sq.:R17N:Astoria-Ditmards Blvd:$YELLOW"
	"1:42 Times Squ.:128N:Van Cortlandt Park-242 St:$RED"
	"2:42 Times Squ.:128N:Wakefield-241 St:$RED"
	"3:42 Times Squ.:128N:Harlem-148 St:$RED"
	"4:Grand Central:631N:Woodlawn:$GREEN"
	"5:Grand Central:631N:Eastchester-Dyre Av:$GREEN"
	"6:Grand Central:631N:Pelham Bay Park:$GREEN"
	"A:Penn. Station:A28N:Inwood-207 St:$BLUE"
	"C:Penn. Station:A28N:168 St:$BLUE"
	"E:Penn. Station:A28N:Jamaica Center-Parsons/Archer:$BLUE"
)

while true
do
	clear
	for info in "${dataUptown[@]}"
	do
		if [ $(echo $info | awk -F':' '{print $1}') == MESSAGE ]; then
			sleep 0.3
			echo ">" $(echo $info | awk -F':' '{print $2}')
		else
			train=$(echo $info | awk -F':' '{print $1}')
			stop=$(echo $info | awk -F':' '{print $2}')
			stopID=$(echo $info | awk -F':' '{print $3}')
			destination=$(echo $info | awk -F':' '{print $4}')
			color=$(echo $info | awk -F':' '{print $5}')

			time=$(python3 APICall.py stops $train --api-key=$APIKEY | grep $stopID | awk '{print $2}')

			if [ -z "$time" ]; then
				time="----- | -------"
			else
				timeSimple=$(echo $time | tr -d ":")
				timeNow=$(date +"%H%M")
				timeDelta=$(expr $timeSimple - $timeNow)
				if [ ${#timeDelta} -gt 2 ]; then
					timeDelta="in 1h+"
				else
					timeDelta="in "$(pad_with_zeros ${#numExample} $timeDelta)m
				fi
			fi

			echo -e ${color}\| $train \|${NC} $time \| $timeDelta \| at $stop \| to $destination
		fi
	done
	sleep 60
done
