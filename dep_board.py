import requests, json, time, datetime, os

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

station_ids = ['D17', 'R17', '127', '631', 'A28']

def gen_stop_dictionary():
    res = requests.get("https://goodservice.io/api/stops")
    api_call = json.loads(res.text)
    res.close()
    output = {}
    for item in api_call["stops"]:
        output[item["id"]] = item["name"]
    return output

station_map = gen_stop_dictionary()

cur_time = time.time()

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
        if station_name not in trains:
            trains[station_name] = {}
        if(direction=="north"):
            lst =  result["upcoming_trips"]["north"]
        else:
            lst =  result["upcoming_trips"]["south"]
        times = [{"station": station_name, "route_id": train['route_id'], "dir": train["direction"], 
                    'dest_stop': train["destination_stop"], "arrival_time": train["current_stop_arrival_time"] }   for train in lst]
#        (station_name, train['route_id'], train['direction'], train['destination_stop'], train["current_stop_arrival_time"])
        trips = {}
        for train in times:
            route_id = train["route_id"]
            if route_id not in found:
                found.append(route_id)
            test_time = train["arrival_time"]
            if route_id not in trips:
                trips[route_id] = train
            else:
                if(test_time <= trips[route_id]["arrival_time"]):
                    trips[route_id] = train
        closest_times.update(trips)
#    print(found)
    return [format_line(closest_times[route]) for route in closest_times]

def format_line(route_dict):
#    output = route_dict[]
    train_color = color_map[route_dict["route_id"]]
    time_delta = time.strftime('%H:%M', time.gmtime(route_dict["arrival_time"]-cur_time))
    military_time = time.strftime('%H:%M', time.localtime(route_dict["arrival_time"]))
    output = train_color+" | "+route_dict["route_id"]+" | "+NoColor+" | "+  military_time + " | in " +time_delta + " | at " + route_dict["station"]
    output += " to " +station_map[route_dict["dest_stop"]]
    print(output)
    return output

def refresh(station_ids):
    api_results  = [gen_json(cur_id) for cur_id in station_ids]
    print("Uptown: The Bronx, & Upper Queens")
    build_station_arrival_times(api_results, "north")
    print("Downtown: Brooklyn & Lower Queens")
    build_station_arrival_times(api_results, "south")
    time.sleep(30)

os.system("clear")
while(True):
    refresh(station_ids)