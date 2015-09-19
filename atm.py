import requests
import json

apiKey = '7705c20d5f3f8ecbbffc78c5cac2a2ff'

while True:
	customerId = '55e94a6cf8d8770528e618ca' #Fingerprint sensor decides
	responseAction = {
		201 : lambda : print('It worked'),
		400 : lambda : print('Uh oh, something in your payload is wrong'),
	}

	url = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(customerId,apiKey)

	req = requests.get(url)
	print(req.json()['balance'])

