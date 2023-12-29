import os,datetime,sys
import pytz
import time

"""

Hacky way of getting departure times from MTA API


"""

from underground import metadata, SubwayFeed

API_KEY = "7dPziNcZAO7I14bR1o5hD1RcW3trloOo1rgN0Vhu" # API key

# Color codes

NoColor = "\033[0m"
Red = "\u001b[31m"
Orange = "\u001b[31;1m"
Green = "\u001b[32m"
Yellow = "\u001b[33m"
Blue = "\u001b[34m"
Purple = "\u001b[35m"


# Indexed by line name
# Color: Train Color
# Station: Train station near HM
# Terminal: Terminating station of the line
# StationID: API Station tag

## S = Downtown, N = Uptown

train_data_map ={
 "B" :
	{ "Color":Orange, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "D17N", "Terminal": "Bedford Park Boulevard"},
    	"Downtown":
		{"StationID": "D17S", "Terminal": "Brighton Beach"}
	},
 "D" :
	{ "Color":Orange, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "D17N", "Terminal": "Norway"},
    	"Downtown":
		{"StationID": "D17S", "Terminal": "Coney Island-Stillwell Av"}
	},
 "F" :
	{ "Color":Orange, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "D17N", "Terminal": "Jamaica"},
    	"Downtown":
		{"StationID": "D17S", "Terminal": "Coney Island-Stillwell Av"}
	},
 "M" :
	{ "Color":Orange, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "D17N", "Terminal": "Forest Hills"},
    	"Downtown":
		{"StationID": "D17S", "Terminal": "Middle Village"}
	},
 "N" :
	{ "Color":Yellow, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "R17N", "Terminal": "Astoria"},
    	"Downtown":
		{"StationID": "R17S", "Terminal": "Coney Island-Stillwell Av"}
	},
 "Q" :
	{ "Color":Yellow, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "R17N", "Terminal": "Astoria"},
    	"Downtown":
		{"StationID": "R17S", "Terminal": "Coney Island-Stillwell Av"}
	},
 "R" :
	{ "Color":Yellow, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "R17N", "Terminal": "Astoria"},
    	"Downtown":
		{"StationID": "R17S", "Terminal": "Coney Island-Stillwell Av"}
	},
 "W" :
	{ "Color":Yellow, "Station": "34 Herald Sq.",
    	"Uptown" :
		{"StationID": "R17N", "Terminal": "Ditmars Blvd"},
    	"Downtown":
		{"StationID": "R17S", "Terminal": "Whitehall St-South Ferry"}
	},
 "1" :
	{ "Color":Red, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "128N", "Terminal": "Van Cortlandt Park"},
    	"Downtown":
		{"StationID": "128S", "Terminal": "South Ferry"}
	},
 "2" :
	{ "Color":Red, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "128N", "Terminal": "Wakefield 241 St."},
    	"Downtown":
		{"StationID": "128S", "Terminal": "Flatbush Av."}
	},
 "3" :
	{ "Color":Red, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "128N", "Terminal": "Harlem 148 St."},
    	"Downtown":
		{"StationID": "128S", "Terminal": "New Lots Av"}
	},
 "4" :
	{ "Color":Green, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "631N", "Terminal": "Woodlawn"},
    	"Downtown":
		{"StationID": "631S", "Terminal": "New Lots Av"}
	},
 "5" :
	{ "Color":Green, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "631N", "Terminal": "Eastchester"},
    	"Downtown":
		{"StationID": "631S", "Terminal": "Flatbush Av"}
	},
 "6" :
	{ "Color":Green, "Station": "42 Times Squ.",
    	"Uptown" :
		{"StationID": "631N", "Terminal": "Pelham Bay"},
    	"Downtown":
		{"StationID": "631S", "Terminal": "Brooklyn Bridge"}
	},
 "A" :
	{ "Color":Blue, "Station": "Penn. Station",
    	"Uptown" :
		{"StationID": "A28N", "Terminal": "Inwood"},
    	"Downtown":
		{"StationID": "A28S", "Terminal": "Rockaway Park"}
	},
 "C" :
	{ "Color":Blue, "Station": "Penn. Station",
    	"Uptown" :
		{"StationID": "A28N", "Terminal": "168th Street"},
    	"Downtown":
		{"StationID": "A28S", "Terminal": "Euclid Av"}
	},
 "E" :
	{ "Color":Blue, "Station": "Penn. Station",
    	"Uptown" :
		{"StationID": "A28N", "Terminal": "Jamaica Center"},
    	"Downtown":
		{"StationID": "A28S", "Terminal": "World Trade Center"}
	},
}

def formate(station_arrival,train):
 print(station_arrival)

def get_data(key,train_data,cur_date_time,  direction="Uptown"):
	s_id = train_data[key][direction]["StationID"]
	feed = SubwayFeed.get(key, api_key=API_KEY)
	datetime_arrival = feed.extract_stop_dict()[key][s_id][0]
	datetime_arrival = datetime_arrival.replace(tzinfo=None)
	arrival_time = datetime_arrival.strftime("%M:%S")
#	print("Arrive: " + repr(datetime_arrival))
#	print("Cur: "+ repr(cur))
	delta =  datetime_arrival-cur_date_time
	delta_time = str(delta).split(".")[0]
#	print(delta_time)
	terminal_output = " | ".join([train_data[key]["Color"], key , NoColor+  arrival_time,
	delta_time, "at "+str(train_data[key]["Station"]),"to "+str(train_data[key][direction]["Terminal"])])
	print(terminal_output)
#	sys.exit()

while(True):
	os.system("clear")
	start_time = time.time()
	cur = datetime.datetime.now()
# hack to turn UTC to EST
	cur = cur.replace(hour = cur.hour + 1)
	cur_datetime_format = str(cur.hour)+":"+str(cur.minute)
	print("Uptown: The Bronx & Upper Queens")
	for train in train_data_map:
		get_data(train,train_data_map,cur,"Uptown")
	print("Downtown: Brooklyn & Lower Queens")
	for train in train_data_map:
		get_data(train,train_data_map,cur,"Downtown")
	while(True):
		cur_time = time.time()
		dt = cur_time-start_time
		if(dt >= 60):
			break
