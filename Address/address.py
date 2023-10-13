import csv
from flask import Flask, request, jsonify
import requests

# whitelist = ["00:11:22:33:44:55", "66:77:88:99:AA:BB"]  # List of allowed Bluetooth device IDs

# convert csv to python dictionaries
with open('tables.csv', mode='r') as infile:
    # the first row are the keys. Convert the rest into python dictionaries
    reader = csv.DictReader(infile)
    # print([rows for rows in reader])
    whitelist = {}
    for item in reader:
        whitelist[item['deviceId']] = item

print(whitelist)
station="CG 1"
station_service_url = 'http://localhost:5002'
sms_service_url = 'http://localhost:5003'

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/getHome/<deviceId>', methods=['GET'])
def homeAddr(deviceId):
    # Check if the device is in the whitelist
    if deviceId in whitelist:
        return jsonify(whitelist[deviceId])
    else:
        return jsonify({"error": "Device not found"}), 404

@app.route('/passRoute', methods=['POST'])
def passRoute():
    data = request.get_json()
    end_station = data.get('homeStn')
    start_station = station
    current_station = station
    deviceId = data.get('deviceId')
    # phone_number = data.get('phoneNo')

    whitelist[deviceId]['startStn'] = start_station
    whitelist[deviceId]['currentStn'] = current_station

    # make a call for the shortest path at port 5000
    request_url = f"{station_service_url}/checkStop"
    response = requests.post(request_url, json={"current_code": current_station, "start_code": start_station, "end_code": end_station})

    resp = response.json()
    print(resp)


    if resp["status"] in [200, 406]:
        print("YAHOO send SMS")
        print(f"Sending to {whitelist[deviceId]['phoneNo']}")
        print(f"Route: {sms_service_url}/sendSMS")
        print({"message": resp['message'], "phone_number": whitelist[deviceId]['phoneNo']})
        # send SMS to user
        request_url = f"{sms_service_url}/sendSMS"
        try:
            sms_response = requests.post(request_url, json={"message": resp['message'], "phone_number": whitelist[deviceId]['phoneNo']})
            print(str(sms_response))
            return jsonify({"status": 200, "message": resp['message']})
        except:
            return jsonify({"status": 500, "error": "Internal Server Error"})
    else:
        return jsonify({"error": "Bad Request"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

