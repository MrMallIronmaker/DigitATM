import os
import json
import locale
import datetime

import requests

API_KEY = '7705c20d5f3f8ecbbffc78c5cac2a2ff'

class RequestManager:
    
    @staticmethod
    def getBalance(customerID):

        """
        Returns a customer's balance
        with normal USD formatting.
        """

        URL = "http://api.reimaginebanking.com/accounts/{}?key={}".format(customerID, API_KEY)
        request = requests.get(URL)
        balance = float(str(request.json()['balance']))
        return locale.currency(balance, grouping=True)

    @staticmethod
    def deposit(customerID, amount):

        """
        Deposit amount in a 
        customer's account.
        """

        payload = {
            "medium": "balance",
            "transaction_date": datetime.datetime.now().strftime("%I:%M%p %B %d, %Y"),
            "status": "completed",
            "amount": amount,
            "description": "Verified with fingerprint."
        }
        
        URL = "http://api.reimaginebanking.com/accounts/{}/deposits?key={}".format(customerID, API_KEY)
        request = requests.post(URL, data=payload)
        for key in request.json().keys():
            print(key, ":", request.json()[key])

    @staticmethod
    def withdraw(customerID, amount):

        """
        Withdraw amount from a 
        customer's account.
        """

        payload  = {
            "medium": "balance",
            "transaction_date": str(datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")),
            "status": "completed",
            "amount": amount,
            "description": "Verified with fingerprint."
        }
        URL = "http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}".format(customerID, API_KEY)
        request = requests.post(URL, data=payload)
        for key in request.json().keys():
            print(key, ":", request.json()[key])

locale.setlocale( locale.LC_ALL, '' )
