import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

username = '*******'
password = '*******'

def get_njt_token(is_test=False):
    # Choose the URL based on the is_test flag
    url = 'https://testraildata.njtransit.com/api/TrainData/getToken' if is_test else 'https://raildata.njtransit.com/api/TrainData/getToken'
    
    # Make the POST request
    response = requests.post(
        url,
        data={
            'username': username,
            'password': password
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
            
            if 'Authenticated' in response_json:
                if response_json['Authenticated'] == "True":
                    return response_json['UserToken']
                else:
                    return None
            elif 'errorMessage' in response_json:
                return None
            else:
                return None
        
        except ValueError:
            return None
    else:
        return None
