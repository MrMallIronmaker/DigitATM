import requests
import json
import os

apiKey = '7705c20d5f3f8ecbbffc78c5cac2a2ff'
with open('accounts.json') as data_file:
	data = json.load(data_file)
file = open('stream.txt', 'r')
char = file.read(1)
flag = False
while True:
	if flag == True:
		file.seek(0)
		char=file.read(1)
		flag = False
	customerId = char #Fingerprint sensor decides
	responseAction = {
		201 : lambda : print('It worked'),
		400 : lambda : print('Uh oh, something in your payload is wrong'),
	}

	url = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(data[customerId],apiKey)

	req = requests.get(url)
	print("Your balance is " + str(req.json()['balance']))
	char = file.read(1)
	if char=='\n':
		os.remove('stream.txt')
	while os.path.isfile("stream.txt") == False: #Waiting for new number in file
		flag = True

