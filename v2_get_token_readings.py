import json
import requests
import pickle
import datetime
from datetime import datetime, timedelta
import os

# api endpoint
url1 = "http://10.0.30.10/api/Auth/authenticate"

# header content
headers = {
    "accept":"application/json",
    "Content-Type":"application/json"
}

# define params; username and pw to retrieve token
params = {
    "username":"admin",
    "password":"DB53EB67"
}

# get auth token from leap gateway
def get_reading():
    resp = requests.post(url1, headers = headers, data=json.dumps(params))
    tk = json.loads(resp.text)['token']

    # set starting time for each reading
    current_time = datetime.now()
    current_minus = current_time - timedelta(minutes=2)
    startDate = current_minus.isoformat() + 'Z'

    # url for getting readings from specific leap sensor
    url2 = f'http://10.0.30.10/ClientApi/V1/DeviceReadings?deviceId=000D6FFFFE3CE2A6&startDate={startDate}'

    # pass token to get readings
    headers2 = {'Authorization': f'Bearer {tk}'}

    # perform get and pass content to variable result
    response = requests.get(
        url2, headers=headers2,
    )

    result = response.content

    # parse reading output to retrieve on the labels and values we need
    pick = json.loads(result.decode("UTF-8"))[0]
    readingTimestamp = (pick.get("readingTimestamp"))
    x = {
            "deviceId": pick.get("deviceId"),
            "readingTimestamp": pick.get("readingTimestamp"),
            "value": pick.get("values")[0].get("value"),
            "label": pick.get("values")[0].get("label")
        }
    sensor_type = {'deviceType': 'Temperature Sensor'}
    x.update(sensor_type)
    return x
    
# Convert last reading from string to json object
def old_stuff(x):
    json_obj = json.dumps(x)
    print(json_obj)

    # write output of 'json_obj' to file
    output_dir = '/home/atosadmin/py-tests/prod'
    output_file = 'output.json'
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, "w") as output_file:
        output_file.write(json_obj)