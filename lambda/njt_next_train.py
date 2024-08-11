import requests
import logging
from datetime import datetime
from njt_token import get_njt_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#    "STATION_2CHAR": "TS",
#    "STATIONNAME": "Secaucus Lower Lvl",

#    "STATION_2CHAR": "SE",
#    "STATIONNAME": "Secaucus Upper Lvl",

#    "STATION_2CHAR": "HB",
#    "STATIONNAME": "Hoboken",

#    "STATION_2CHAR": "NY",
#    "STATIONNAME": "New York Penn Station",

def construct_sentence(trains):
    sentences = []
    sentences.append(f"Okay, here are your next options!")
    for i, train in enumerate(trains, start=1):
        sentences.append(f"A train departs at {train['SCHED_DEP_DATE']} from Track {train['TRACK']}.")
    return " ".join(sentences)


def depart_from_my_home(from_station="TS", to_station="Hoboken", is_test=False):
    
    token = get_njt_token(is_test)
    if token is None:
        return "Sorry, I don't know the next train to " + to_station
        
    # Choose the URL based on the is_test flag
    url = 'https://testraildata.njtransit.com/api/TrainData/getTrainSchedule' if is_test else 'https://raildata.njtransit.com/api/TrainData/getTrainSchedule'
    
    # Make the POST request
    response = requests.post(
        url,
        data={
            'token': token,
            'station': from_station
        },
        headers={
            'Accept': 'text/plain'
        }
    )
    # logger.info(response)
    
    # Check the response
    if response.status_code == 200:
        try:
            response_json = response.json()
            
            # Extract items
            items = response_json.get("ITEMS", [])
            
            # Filter items with destination "Hoboken"
            hoboken_items = [item for item in items if item.get("DESTINATION") == to_station]
            
            # Sort by SCHED_DEP_DATE (assuming format is consistently sortable)
            hoboken_items.sort(key=lambda x: x.get("SCHED_DEP_DATE", ""))
            
            # Get top 3 items
            top_3_items = hoboken_items[:3]
            
            # Extract and print SCHED_DEP_DATE and TRACK
            result = [{"SCHED_DEP_DATE": datetime.strptime(item["SCHED_DEP_DATE"], "%d-%b-%Y %I:%M:%S %p").strftime("%I:%M %p"), "TRACK": item["TRACK"]} for item in top_3_items]
            
            # Get the constructed sentence
            sentence = construct_sentence(result)
            
            return sentence
        
        except ValueError:
            return None
    else:
        return None
