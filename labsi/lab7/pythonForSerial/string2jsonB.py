import json
#from collections import defaultdict

def string2json(filename):
	

		f = open(filename, "r")
		line = f.readline()
		f.close()

		items = []

		for item in line.split("!"):
			items.append(item)

		elements = []
		for item in items[:-1]:
			(info, timestamp) = item.split(";")
			elements.append((info, timestamp))
		print(elements)

		#so all the input is terminating in ';' therefore I don't need the last item

		listOfPairs = []
		
		for info, timestamp in elements:
			print(info)
			(key, value) = info.split("~")
			listOfPairs.append((key, (value, timestamp)))

		#print(listOfPairs)

		myDict = {} #with added values
		for (key, (value, timestamp)) in listOfPairs:
			if key in myDict:
				myDict[key].append([value, timestamp])
			else:
				myDict[key] = [[value, timestamp]]
		#print(json.dumps(myDict))

		#For plotly.js:
		dictPlotlyTemperature = {'x':[], 'y':[], 'name':'temperature', 'type': 'scatter'}
		dictPlotlyHumid = {'x':[], 'y':[], 'name':'humidity', 'type': 'scatter'}
		dictPlotlyCo2 = {'x':[], 'y':[], 'name':'co2Level', 'type': 'scatter'}


		if 'temperature' in myDict.keys():
			for [value, timestamp] in myDict['temperature']:
				dictPlotlyTemperature['x'].append(timestamp)
				dictPlotlyTemperature['y'].append(value)

		if 'humidity' in myDict.keys():
			for [value, timestamp] in myDict['humidity']:
				dictPlotlyHumid['x'].append(timestamp)
				dictPlotlyHumid['y'].append(value)

		if 'co2_level' in myDict.keys():
			for [value, timestamp] in myDict['co2_level']:
				dictPlotlyCo2['x'].append(timestamp)
				dictPlotlyCo2['y'].append(value)



		bigDict = []
		if 'temperature' in myDict.keys():
			bigDict.append(dictPlotlyTemperature)

		if 'humidity' in myDict.keys():
			bigDict.append(dictPlotlyHumid)

		if 'co2_level' in myDict.keys():
			bigDict.append(dictPlotlyCo2)

		print(json.dumps(bigDict))


		finput=open('/www/pages/data.json', 'w+')
		finput.write(json.dumps(bigDict))
		finput.close()


