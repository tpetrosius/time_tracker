import json

def get_json_data():
	"""Opens json file and retrieves the data"""
	
	with open(r'C:\Users\Vartotojas\Desktop\github\Time Tracker\activities.json', 'r') as json_file:
		data_read = json.load(json_file)
		
		return data_read
		
def write_data_to_json(data_read):
	"""Writes new data to json file"""
	
	with open(r'C:\Users\Vartotojas\Desktop\github\Time Tracker\activities.json', 'w') as json_file:
		json.dump(data_read, json_file, sort_keys=True, indent=4)
