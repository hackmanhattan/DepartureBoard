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

dataDowntown=(
	"MESSAGE:Downtown, Brooklyn, & Lower Queens:"
	"B:34 Herald Sq.:D17S:Brighton Beach:$ORANGE"
	"D:34 Herald Sq.:D17S:Coney Island-Stillwell Av:$ORANGE"
	"F:34 Herald Sq.:D17S:Coney Island-Stillwell Av:$ORANGE"
	"M:34 Herald Sq.:D17S:Middle Village-Metropolitan Av:$ORANGE"
	"N:34 Herald Sq.:R17S:Coney Island-Stillwell Av:$YELLOW"
	"Q:34 Herald Sq.:R17S:Coney Island-Stillwell Av:$YELLOW"
	"R:34 Herald Sq.:R17S:Bay Ridge-95 St:$YELLOW"
	"W:34 Herald Sq.:R17S:Whitehall St-South Ferry:$YELLOW"
	"1:42 Times Squ.:128S:South Ferry:$RED"
	"2:42 Times Squ.:128S:Flatbush Av - Brooklyn College:$RED"
	"3:42 Times Squ.:128S:New Lots Av:$RED"
	"4:Grand Central:631S:New Lots Av:$GREEN"
	"5:Grand Central:631S:Flatbush Av - Brooklyn College:$GREEN"
	"6:Grand Central:631S:Brooklyn Bridge-Cty Hall:$GREEN"
	"A:Penn. Station:A28S:Rockaway Park-Beach 116 St:$BLUE"
	"C:Penn. Station:A28S:Euclid Av:$BLUE"
	"E:Penn. Station:A28S:World Trade Center:$BLUE"
)

while true
do
	clear
	for info in "${dataDowntown[@]}"
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

			time=$(./underground stops $train --api-key=$APIKEY | grep $stopID | awk '{print $2}')

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
