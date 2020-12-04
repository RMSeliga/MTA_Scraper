import csv
import requests

#setting invalid to true so that we loop until a valid response is given
invalid = True
while (invalid):
	line = input("Please choose a line among the following ones: 1-7, A-G, J, L, M, N, Q, R, S, W, Z, SIR: ")
	#this is the set of proper responses
	properset = {'1','2','3','4','5','6','7','A','B','C','D','E','F','G','J','L','M','N','Q','S','Z','R','W','SIR'}
	if (line not in properset):
		print ('Thats not right! Please enter a valid value.')
	else:
		#the user have given a valid response and can move on
		invalid = False
print('Stops of the ' + line + ' route:')
#creating an empty array to store the id's of the stops in
urlStops = []
#sending a get request to the callback that is used on http://subwaytime.mta.info/ to send all the stop info for a chosen route
url = "http://traintimelb-367443097.us-east-1.elb.amazonaws.com/getStationsByLine/" + line + "?callback=angular.callbacks._1"
response = requests.get(url)
#take the response and split it on \, this leaves a lot of 'garbage' but will also allow us to easily access the ids we need
arr = response.text.split("\\")
x = range(len(arr))
#looping through the array we just created
for i in x:
	#if the index we are looking at has a value of id, then the next value will be ':', and the one after that will be the actual id so i+2
	if arr[i] == '\"id':
		#add the id to the array and remove a leading double quote
		urlStops.append(arr[i+2].strip('\"'))
#now we finally get to the csv and open it
with open('stops.txt', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	#for each id in our urlStops we will find the corresponding row in stops.txt
	for station in urlStops:
		#this resets us to the top of the file after each search, so that rows are printed in order and not only 1 row is printed
		csvfile.seek(0)
		for row in spamreader:
			#we want stations not stops
			if (row[4]=='1'):
				#if the id of the row matches the id from urlStops, the row is desired in the printout
				if (row[0] == station):
					#printing the formatted row
					print('- ' + row[1] + "(" + row[0] + ")" + ': ' + row[2] + ',' + row[3])
