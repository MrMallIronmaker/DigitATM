import json

import tornado.ioloop
import tornado.web

from requestManager import RequestManager

ERROR_MESSAGE = "Fuck. This wasn't supposed to happen."

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("index.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("debug.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class BalanceHandler(tornado.web.RequestHandler):
    def post(self):
        customerID = self.get_argument("customerID", "")
        jsondata = None
        with open("accounts.json", "r") as jsonfile:
            jsondata = json.load(jsonfile)
        customerHash = None
        if jsondata is not None and customerID in jsondata:
            customerHash = jsondata[customerID]
        else:
            self.write("Customer ID {0} is not a valid customer ID.".format(customerID))
            return
        if customerHash is not None:
            balance = RequestManager.getBalance(customerHash)
        else:
            self.write("Although customer ID {0} exists, an error occurred when attempting to get the hash value for customer ID {0}.".format(customerID))
            return
        if balance is not None:
            self.write("Customer ID: {0}\nBalance: {1}".format(customerID, balance))
            return
        self.write("Customer ID {0} and its corresponding hash exist. However, the balance for this customer could not be determined.".format(customerID))
            

class WithdrawHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the withdraw handler!")

class DepositHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the deposit handler!")

def my_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/debug", DebugHandler),
        (r"/balance", BalanceHandler),
        (r"/withdraw", WithdrawHandler),
        (r"/deposit", DepositHandler),
    ])

if __name__ == "__main__":
    app = my_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
