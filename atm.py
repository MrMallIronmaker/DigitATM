import requests
import json
import os
import locale
import datetime

apiKey = '7705c20d5f3f8ecbbffc78c5cac2a2ff'
with open('accounts.json') as data_file:
	dis = json.load(data_file)
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
	url = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(dis[customerId],apiKey)

	req = requests.get(url)
	print("Your balance is " + str(req.json()['balance']))
	request = input('Enter 1 for withdrawal, 2 for deposit: ')
	if request=="1":
		amount = input('How much: ')
		if int(amount) > req.json()['balance']:
			print("Lol nope")
		else:	
			payload = {"medium": "balance","amount": int(amount)}
			print(payload)
			URL = "http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}".format(dis[customerId], apiKey)
			request = requests.post(URL, data=payload)
			for key in request.json().keys():
				print(key, ":", request.json()[key])
	else:
		total = input('How much: ')
		payload = {"medium": "balance","amount": int(total)}
		print(payload)
		URL = "http://api.reimaginebanking.com/accounts/{}/deposits?key={}".format(dis[customerId], apiKey)
		request = requests.post(URL, data=json.dumps(payload))
		for key in request.json().keys():
			print(key, ":", request.json()[key])





	char = file.read(1)
	if char=='\n':
		os.remove('stream.txt')
	while os.path.isfile("stream.txt") == False: #Waiting for new number in file
		flag = True

