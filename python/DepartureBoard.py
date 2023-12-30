import os,datetime,sys

from nyct_gtfs import NYCTFeed

# Load the realtime feed from the MTA site

"""
Hacky way of getting departure times from MTA API.

S***** I***** isn't queried for though. Why ask for something that doesn't exist?

"""

API_KEY = "7dPziNcZAO7I14bR1o5hD1RcW3trloOo1rgN0Vhu" # Probably should just be a raw string... meh

# Grouped by color of trains. 7 doesn't work, and I haven't figured out LIRR yet (both should be feasible though?)
API_Endpoints = [
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',
'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr",
]

# Color codes for terminal output

NoColor = "\033[0m"
Red = "\u001b[31m"
Orange = "\u001b[31;1m"
Green = "\u001b[32m"
Yellow = "\u001b[33m"
Blue = "\u001b[34m"
Purple = "\u001b[35m"

# Map station id names to human-interpretable names
station_name_map = {"127S": "42th Times Sq. ", "127N": "42th Times Sq. ",
"D17N": "34th Herald Sq.", "D17S": "34 Herald Sq.  ", 
"R17N": "34th Herald Sq.", "R17S": "34 Herald Sq.  ", 
"631N": "Grand Central  ","631S": "Grand Central  ",
"A28N":"Penn. Station  ","A28S":"Penn. Station  ",

}

# Map 1 letter direction to longer form direction
dir_map = {"S": "Downtown ", "N": "Uptown "}

# Data on nearby stations to HM
nearby_stations = [
{"Line": "B", "Dir": "N", "Station": "D17N", "Color": Orange},
{"Line": "B", "Dir": "S", "Station": "D17S", "Color": Orange},
{"Line": "D", "Dir": "N", "Station": "D17N", "Color": Orange},
{"Line": "D", "Dir": "S", "Station": "D17S", "Color": Orange},
{"Line": "F", "Dir": "N", "Station": "D17N", "Color": Orange},
{"Line": "F", "Dir": "S", "Station": "D17S", "Color": Orange},
{"Line": "M", "Dir": "N", "Station": "D17N", "Color": Yellow},
{"Line": "M", "Dir": "S", "Station": "D17S", "Color": Yellow},
{"Line": "Q", "Dir": "N", "Station": "R17N", "Color": Yellow},
{"Line": "Q", "Dir": "S", "Station": "R17S", "Color": Yellow},
{"Line": "N", "Dir": "N", "Station": "R17N", "Color": Yellow},
{"Line": "N", "Dir": "S", "Station": "R17S", "Color": Yellow},
{"Line": "R", "Dir": "N", "Station": "R17N", "Color": Yellow},
{"Line": "R", "Dir": "S", "Station": "R17S", "Color": Yellow},
{"Line": "W", "Dir": "N", "Station": "R17N", "Color": Yellow},
{"Line": "W", "Dir": "S", "Station": "R17S", "Color": Yellow},
{"Line": "1", "Dir": "N", "Station": "127N", "Color": Red},
{"Line": "1", "Dir": "S", "Station": "127S", "Color": Red},
{"Line": "2", "Dir": "N", "Station": "127N", "Color": Red},
{"Line": "2", "Dir": "S", "Station": "127S", "Color": Red},
{"Line": "3", "Dir": "N", "Station": "127N", "Color": Red},
{"Line": "3", "Dir": "S", "Station": "127S", "Color": Red},
{"Line": "7", "Dir": "N", "Station": "127N", "Color": Purple},
{"Line": "7", "Dir": "S", "Station": "127S", "Color": Purple},
{"Line": "4", "Dir": "N", "Station": "631N", "Color": Green},
{"Line": "4", "Dir": "S", "Station": "631S", "Color": Green},
{"Line": "5", "Dir": "N", "Station": "631N", "Color": Green},
{"Line": "5", "Dir": "S", "Station": "631S", "Color": Green},
{"Line": "6", "Dir": "N", "Station": "631N", "Color": Green},
{"Line": "6", "Dir": "S", "Station": "631S", "Color": Green},
{"Line": "A", "Dir": "N", "Station": "A28N", "Color": Blue},
{"Line": "A", "Dir": "S", "Station": "A28S", "Color": Blue},
{"Line": "C", "Dir": "N", "Station": "A28N", "Color": Blue},
{"Line": "C", "Dir": "S", "Station": "A28S", "Color": Blue},
{"Line": "E", "Dir": "N", "Station": "A28N", "Color": Blue},
{"Line": "E", "Dir": "S", "Station": "A28S", "Color": Blue},
]

# Setup initial API queries
def init_feeds(endpoints):
	return [NYCTFeed(endpoint,api_key= API_KEY) for endpoint in endpoints]

def refresh_feeds(feeds):
	for feed in feeds:
		feed.refresh()

# function to see what the station IDs correspond to what names. Kind of broken right now
def print_station_names(feed,dictionary):
	line = feed.filter_trips(line_id=dictionary["Line"], travel_direction=dictionary["Dir"], headed_for_stop_id=dictionary["Station"])
	print([[(v.stop_name,v.stop_id) for v in t.stop_time_updates] for t in line])

# The heart of program. Given some train data, extract information and format it for terminal
def format_trip(trip, dictionary, current_time):
	for stop in trip.stop_time_updates:
		if(stop.stop_id==dictionary["Station"]):
			delta = format_delta(stop.arrival- current_time)
			terminal_output = " | ".join([dictionary["Color"], dictionary["Line"] ,
				 NoColor+  stop.arrival.strftime("%H:%M:%S"),delta,
				"at "+station_name_map[dictionary["Station"]],
				dir_map[dictionary["Dir"]]+"to "+trip.headsign_text])
			return terminal_output
	return ""

# Convert timedelta to HH:MM:SS
def format_delta(time_delta):
	s = time_delta.seconds
	hours, remainder = divmod(s, 3600)
	minutes, seconds = divmod(remainder, 60)
	out = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
	return out

# Given a RTS feed and a dictionary of train data, see if train will arrive at nearby station
def filter_feed(feed,dictionary, current_time):
	routes = feed.filter_trips(line_id=dictionary["Line"], travel_direction=dictionary["Dir"])
	if(len(routes) ==0):
		return ""
	for line in routes:
		if(line.headed_to_stop(dictionary["Station"])):
			return format_trip(line,dictionary, current_time)
			break
	terminal_output = " | ".join([dictionary["Color"],
	 dictionary["Line"] , NoColor+  "--------","--------","at "+station_name_map[dictionary["Station"]], dir_map[dictionary["Dir"]]+"to Nowhere"])
	return terminal_output

def update_board(feeds,nearby_stations):
# Yes, this is a stupid way of doing things. It works.
# It also doesn't show trains that don't have any routes, like the B on weekends
# We don't care about these though

# it also doesn't work on the 7 since the API request is broken there
# I havn't tried doing the LIRR though at Grand Central
	cache = []
	cur_time = datetime.datetime.now()
	for feed in feeds:
		for station in nearby_stations:
			tag= filter_feed(feed, station, cur_time)
			if tag:
				cache.append(tag)
	[print(line) for line in cache]

if __name__ == "__main__":
	feeds = init_feeds(API_Endpoints)
	refresh_rate = 60
	while(True):
		os.system("clear")
		refresh_start_time = datetime.datetime.now()
		update_board(feeds,nearby_stations)
		refresh_end_time = datetime.datetime.now()
		delta = refresh_end_time-refresh_start_time
		while(True):
			if(delta.seconds < refresh_rate):
				refresh_feeds(feeds)
				refresh_end_time = datetime.datetime.now()
				delta = refresh_end_time-refresh_start_time
			else:
				break		
