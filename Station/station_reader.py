from flask import Flask, jsonify, request
from MRT_Classes import Station, MetroMap
from sgMrt import stations_data

app = Flask(__name__)

@app.route('/checkStop', methods=['POST'])
def getMessage():
	current_code, start_code, end_code=None, None, None

	data = request.get_json()
	current_code = data.get('current_code')
	start_code = data.get('start_code')
	end_code = data.get('end_code')

	if(current_code==None or start_code==None or end_code == None):
		return jsonify({
				"status": 400,
				"error": "Bad Request: Missing parameters"
			})


	path, changes = mrt_map.find_shortest_path(start_code, end_code)
	# print(f"Path: {path}")
	# print(f"Change: {[(item[0].__str__(), item[1].__str__()) for item in changes]}")

	if current_code not in path:
		path, changes = mrt_map.find_shortest_path(current_code, end_code)
		# print("------ change path!=======")
		# print(f"Path: {path}")
		# print(f"Change: {[(item[0].__str__(), item[1].__str__()) for item in changes]}")
		
		next_stop=path[0]
		next_line=mrt_map.stations[path[0]].line
		data = {"start_code": current_code}
		return jsonify({"status":406, 
			"error": "Not Acceptable: Current station code not in path.",
			"message": f"You have gotten off-track. Please proceed back on track by boarding {next_stop} at the {next_line} line",
			"data":data
			})

	# Convert the tuples to lists for JSON serialization
	changes_as_lists = [[s1, s2] for s1, s2 in changes]

	for s1, s2 in changes:
		if current_code == s1.code:
			return jsonify({
				"status": 200,
				'message': f'Please change lines here. You are currently at {s1.code} {s1.name} station on the {s1.line} line, kindly head to the platform for the {s2.line} line.'
				})
		get_off_next = False

		for stn in path[::-1]:
			if stn == s1.code:
				get_off_next = True
			if get_off_next and stn==current_code:
				return jsonify({
					"status": 200,
					"message": f"You are currently at {current_code}, please be ready to get off at {s1.code} {s1.name} on the next stop to change to the {s2.line} line."
					})
		# print(f"Second to last stop is {path[-2]}")
		if current_code==path[-2]:
			return jsonify({
				"status": 200,
				"message": f"You are reaching destination {end_code}. Please be ready to alight from the train and tap out."
				})

	else:
		if(current_code==end_code):
			return jsonify({
				"status": 200,
				"message": "You have reached your destination. Please get off at this station and proceed to the gantry to tap out."
				})


		return jsonify({
			"status": 204,
			'message': 'No change needed at this station.'
			})

if __name__ == '__main__':
	mrt_map = MetroMap(stations_data)
	app.run(host='0.0.0.0', debug=True)
