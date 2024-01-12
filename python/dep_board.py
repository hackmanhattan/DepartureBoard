import requests
import json
import time
import datetime
import os
import sys

# Color codes for terminal output

NoColor = "\u001b[37m"
Red = "\u001b[31m"
Orange = "\u001b[31;1m"
Green = "\u001b[32m"
Yellow = "\u001b[33m"
Blue = "\u001b[34m"
Purple = "\u001b[35m"

# Mapping each train/route name to a color code (GS mapped to Green)
color_map = {
    "B": Orange,
    "D": Orange,
    "F": Orange,
    "M": Orange,
    "Q": Yellow,
    "N": Yellow,
    "R": Yellow,
    "W": Yellow,
    "1": Red,
    "2": Red,
    "3": Red,
    "7": Purple,
    "4": Green,
    "5": Green,
    "6": Green,
    "GS": Green,
    "A": Blue,
    "C": Blue,
    "E": Blue,
    }

# The station IDs
station_ids = ['D17', 'R17', 
    '127', '902','R16','725',
    '724', 
    '631', '723','901',
    'A28', '128']

# Mapping the station ID to a fixed-width station name
nearby_station_ids = {
    'D17': "34 Herald Sq.",
    "R17": "34 Herald Sq.",
    "127": "42 Times Squ.",
    "902": "42 Times Squ.",
    "R16": "42 Times Squ.",
    "725": "42 Times Squ.",
    "724": "5th Av.      ",
    "631": "Grand Central",
    "723": "Grand Central",
    "901": "Grand Central",
    "A28": "Penn. Station",
    "128": "Penn. Station"}


def gen_stop_dictionary():
# Polls API for all stations, and creates dictionary with station_id as key
    res = requests.get("https://goodservice.io/api/stops")
    api_call = json.loads(res.text)
    res.close()
    output = {}
    for item in api_call["stops"]:
        output[item["id"]] = item["name"]
    return output


def get_station_data(station_id):
# returns raw json from API call for a given station
    break_out = 1
    while break_out:
        try:
            res = requests.get('https://goodservice.io/api/stops/' + station_id)
            break_out = 0
        except:
# Request failed for whatever reason. Wait, then try again. You can get stun locked though... o' well.
            res.close()
            time.sleep(5)
    api_call = json.loads(res.text)
    return api_call


def build_station_arrival_times(api_results, direction):
## Given dictionary of station IDs and North/southbound status, print available trains
# Key for closest_times is the train_id, while the values are just the relevant values from the api_results (see all_stations list comprehension)
    closest_times = {}
    for result in api_results:
# Grab the stations for a given train depending on up/downtown status
        station_name = result["name"]
        nearby_station_id = result["id"]
        if (direction == "north"):
            lst = result["upcoming_trips"]["north"]
        else:
            lst = result["upcoming_trips"]["south"]
# For all the stations on a given trains line, grab all the required variables. Each item in this list is a station
        all_stations = [{"station": station_name,
                  "station_id": nearby_station_id,
                  "route_id": train['route_id'],
                  "dir": train["direction"],
                  'dest_stop': train["destination_stop"],
                  "arrival_time": train["current_stop_arrival_time"]} for train in lst]
# Re organize all_stations to be indexed by train_id/route instead
        trips = {}
        for train in all_stations:
            route_id = train["route_id"]
            test_time = train["arrival_time"]
            if route_id not in trips:
                trips[route_id] = [train]
            else:
                trips[route_id].append(train)
        closest_times.update(trips)
# Sort trains by color after formatting, then print to screen
    trains_to_sort = []
    for train_id in closest_times:
        trains_to_sort.append(format_line(closest_times[train_id]))
    trains_to_sort.sort()
# Join item in trains_to_sort with new lines
    catted_string = '\n'.join(trains_to_sort)
    print(catted_string)


def format_line(route_list):
    route_list.sort(key=lambda x: x["arrival_time"])
# Grab the train color from closest arriving train
    route = route_list[0]
    train_color = color_map[route["route_id"].replace("X", "")]
# Store time deltas (ie. different between arrival time and current time)
    time_ds = []
# Limit results to next 3 trains
    closest_arrival_time = time.strftime('%H:%M', time.localtime( route_list[0]["arrival_time"]))
    for hit in route_list[:3]:
# Convert UNIX-epoch time to H:M format for arrival time of train
        military_time = time.strftime('%H:%M', time.localtime( hit["arrival_time"]))
# Format time_delta appropriately (greater than 1hr, list as hr+, otherwise, use minutes. 00 means leaving now)
        tds = time.gmtime(hit["arrival_time"] -cur_time)
        hr = int(time.strftime("%H", tds))
        if(hr > 0):
            time_ds.append("hr+")
        else:
            time_ds.append(time.strftime('%Mm',tds) )
# Janky way of dealing with fewer than 3 stations being displayed
    if len(time_ds) < 3:
        for i in range(3 - len(time_ds)):
            time_ds.append("---")
# concatenate all the time delta strings
    time_delta = ", ".join(time_ds)
# Edge cases: X means express line, so need to mess with width of route["route_id"]. GS obeys same rules as express lines
    if (("X" in route["route_id"]) or ("GS" in route["route_id"]) ):
        output = train_color + " | " + route["route_id"] + " | " + NoColor + " | " + \
            closest_arrival_time + " | in " + time_delta + " | at " + nearby_station_ids[route["station_id"]]
    else:
        output = train_color + " | " + route["route_id"] + "  | " + NoColor + " | " + \
            closest_arrival_time + " | in " + time_delta + " | at " + nearby_station_ids[route["station_id"]]
    output += "| to " + station_map[route["dest_stop"]]
    return output

def refresh(station_ids):
## refreshes information from API
# Grab all relavent stations from API
    api_results = [get_station_data(cur_id) for cur_id in station_ids]
# Format current time to screen
    os.system("date +\"%H:%M\" | figlet")
# Get data and print to screen
    print("Uptown: The Bronx, & Upper Queens")
    build_station_arrival_times(api_results, "north")
    print("Downtown: Brooklyn & Lower Queens")
    build_station_arrival_times(api_results, "south")
# Wait so that we don't get banned
    time.sleep(30)
# Clear screen
    os.system("clear")

if __name__ == "__main__":
    station_map = gen_stop_dictionary()
## Print out all the stations in the subway, then exit. Use grep to find the appropriate station ID
#    print(station_map)
#    sys.exit()
    cur_time = time.time()
    os.system("clear")
    while (True):
        refresh(station_ids)
        cur_time = time.time()
