import requests, json, time, datetime, os, sys

# Color codes for terminal output

NoColor = "\033[0m"
Red = "\u001b[31m"
Orange = "\u001b[31;1m"
Green = "\u001b[32m"
Yellow = "\u001b[33m"
Blue = "\u001b[34m"
Purple = "\u001b[35m"

color_map = {"B":Orange, "D": Orange, "F": Orange, "M": Yellow, "Q": Yellow, "N": Yellow, "R": Yellow, "W": Yellow,
"1": Red, "2": Red, "3": Red, "7": Purple, "4": Green, "5": Green, "6": Green, "A": Blue, "C": Blue, "E": Blue}

station_ids = ['D17', 'R17', '127', '631', 'A28', '724']

nearby_station_ids = {'D17': "34 Herald Sq.", "R17":"34 Herald Sq.",
 "127":"42 Times Squ.","724":"5th Av.      ","631":"Grand Central", "A28":"Penn. Station"}

def gen_stop_dictionary():
    res = requests.get("https://goodservice.io/api/stops")
    api_call = json.loads(res.text)
    res.close()
    output = {}
    for item in api_call["stops"]:
        output[item["id"]] = item["name"]
    return output

def gen_json(url):
    res = requests.get('https://goodservice.io/api/stops/'+url)
    api_call = json.loads(res.text)
    res.close()
    return api_call

def build_station_arrival_times(api_results, direction):
    trains = {}
    closest_times = {}
    found = []
    for result in api_results:
        station_name = result["name"]
        nearby_station_id = result["id"]
        if station_name not in trains:
            trains[station_name] = {}
        if(direction=="north"):
            lst =  result["upcoming_trips"]["north"]
        else:
            lst =  result["upcoming_trips"]["south"]
        times = [{"station": station_name,"station_id": nearby_station_id , "route_id": train['route_id'], "dir": train["direction"], 
                    'dest_stop': train["destination_stop"], "arrival_time": train["current_stop_arrival_time"] }   for train in lst]
#        (station_name, train['route_id'], train['direction'], train['destination_stop'], train["current_stop_arrival_time"])
        trips = {}
        for train in times:
            route_id = train["route_id"]
            if route_id not in found:
                found.append(route_id)
            test_time = train["arrival_time"]
            if route_id not in trips:
## Single Stop
#                trips[route_id] = train
## Multi Stop
                trips[route_id] = [train]
            else:
## Single Stop
#                if(test_time <= trips[route_id]["arrival_time"]):
#                    trips[route_id] = train
## Multi Stop
                if(len(trips[route_id]) < 3):
                    trips[route_id].append(train)
        closest_times.update(trips)
#    print(found)
    for route in closest_times:
        format_line(closest_times[route])

def format_line(route_list):
#    output = route_list[]
    route_list.sort(key = lambda x: x["arrival_time"])
    route = route_list[0]
    train_color = color_map[route["route_id"].replace("X","")]
    military_time = time.strftime('%H:%M', time.localtime(route["arrival_time"]))
## Single Line
#    time_delta = time.strftime('%H:%M', time.gmtime(route_list["arrival_time"]-cur_time))
## MultiLine
    time_ds = [time.strftime('%Mm', time.gmtime(hit["arrival_time"]-cur_time)) for hit in route_list]
    time_delta = ",".join(time_ds)
    if("X" in route["route_id"]):
        output = train_color+" | "+route["route_id"]+" | "+NoColor+" | "+  military_time + " | in " +time_delta + " | at " + nearby_station_ids[route["station_id"]]
    else:
        output = train_color+" | "+route["route_id"]+"  | "+NoColor+" | "+  military_time + " | in " +time_delta + " | at " + nearby_station_ids[route["station_id"]]
    output += "| to " +station_map[route["dest_stop"]]
    cmd = "echo \"" + output + "\""
    os.system(cmd)
#    print(output)
    return output

def refresh(station_ids):
    api_results  = [gen_json(cur_id) for cur_id in station_ids]
    os.system("date +\"%H:%M\" | figlet | lolcat")
    print("Uptown: The Bronx, & Upper Queens")
    build_station_arrival_times(api_results, "north")
    print("Downtown: Brooklyn & Lower Queens")
    build_station_arrival_times(api_results, "south")
    time.sleep(30)
    os.system("clear")


if __name__ == "__main__":
    station_map = gen_stop_dictionary()
    cur_time = time.time()
    os.system("clear")
    while(True):
        refresh(station_ids)