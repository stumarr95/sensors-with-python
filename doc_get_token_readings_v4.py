import json
import requests
import pickle
import datetime
from datetime import datetime, timedelta
import os

# api endpoints
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

    # nextDate = '2023-03-14T16:30:20Z'
    url2 = f'http://10.0.30.10/ClientApi/V1/DeviceReadings?deviceId=000D6FFFFE3AAFA9&startDate={startDate}'

    # pass token to get readings
    headers2 = {'Authorization': f'Bearer {tk}'}

    # perform get and print content
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
            "value": pick.get("values")[1].get("value"),
            "label": pick.get("values")[1].get("label")
        }
    door_value = x['value']
    door_value_reading = {'door_status': door_value}

    # adding deviceType variable to identify sensor type in RIoT
    sensor_type = {'deviceType': 'Door Sensor'}

    x.update(door_value_reading)
    x.update(sensor_type)
    del x["value"]
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