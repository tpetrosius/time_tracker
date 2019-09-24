import win32api, win32gui, win32process, wmi
import datetime
from pywinauto import Application
from manipulate_json import get_json_data, write_data_to_json

def convert_duration(duration):
	days = duration.days
	seconds = duration.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60
	
	return days, hours, minutes, seconds

def structure_data(start_time, end_time, days, hours, minutes, seconds):
	activity = {
				'start_time' : start_time.strftime("%Y-%m-%d %H:%M:%S"),
				'end_time' : end_time.strftime("%Y-%m-%d %H:%M:%S"),
				'days' : days,
				'hours' : hours,
				'minutes' : minutes,
				'seconds' : seconds,
				}
	
	return activity

#Get data from JSON file
try:
	data_read = get_json_data()
except Exception:
	print('JSON file was not found.')

activity = ''
new_activity = ''
first_time = True

c = wmi.WMI()
try:
	while True:
		#Get application name
		new_window_hwnd = win32gui.GetForegroundWindow()
		_, pid = win32process.GetWindowThreadProcessId(new_window_hwnd)
		for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
			exe = p.Name
			activity = exe.replace('.exe', '').title()
		#If Google Chrome get active url address
		if activity == 'Chrome':
			try:
				app = Application(backend='uia')
				app.connect(title_re=".*Chrome.*")
				dlg = app.top_window()
				url = dlg.child_window(title="Adreso ir paieškos juosta", control_type="Edit").get_value()
				website = url.split('/')[0]
				activity = website
			except Exception:
				continue

		#Check if previous activity is the same as current activity	
		if new_activity != activity:
			
			#Count time entries and write data to JSON	
			if not first_time:
				end_time = datetime.datetime.now()
				duration = end_time - start_time
				days, hours, minutes, seconds = convert_duration(duration)
				time_entries = structure_data(start_time, end_time, days, hours, minutes, seconds)
				
				length = len(data_read['activities'])
				exists = False

				#Append new data to json
				#If activity is found in JSON then append only time entries
				for i in range(0, length):
					if data_read['activities'][i]['name'] == new_activity:
						exists = True
						data_read['activities'][i]['time_entries'].append(time_entries)
				
				#If activity is not found in JSON then add activity and time entries		
				if not exists:
					entry = {
							"name" : new_activity,
							"time_entries" : [time_entries]
							}
					data_read['activities'].append(entry)
				
				#Write new data to JSON
				write_data_to_json(data_read)
				
			first_time = False
			start_time = datetime.datetime.now()
			new_activity = activity
			print(new_activity)
			
		else:
			continue

except KeyboardInterrupt:
	write_data_to_json(data_read)
