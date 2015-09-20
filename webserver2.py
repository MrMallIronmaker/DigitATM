import locale
import json

import tornado.ioloop
import tornado.web

from requestManager import RequestManager
from matlab import engine

ERROR_MESSAGE = "Fuck. This wasn't supposed to happen."

eng = engine.start_matlab()
eng.cd('matlab')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("hold.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.set_cookie("digitATM", "")
        self.write(data)

class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("debug.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class TryAgainHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("tryagain.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class NoMatchHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("nomatch.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class MenuHandler(tornado.web.RequestHandler):
    def get(self):
        # reroute depending on success of matlab call
        data = None
        cookieID = self.get_cookie("digitATM")
        if (cookieID == ""):
            printID = eng.print_match()
            if printID == -1: # nothing there. try again.
                self.redirect(r"/tryagain")
                return
            elif printID == 0: # no match
                self.redirect(r"/nomatch")
                return
            else:
                # convert to user ID and store it in the cookie
                # you have no idea how pathetic this practice is
                printID = str(int(printID))

                jsondata = None
                with open("accounts.json", "r") as jsonfile:
                    jsondata = json.load(jsonfile)
                customerID = None
                if jsondata is not None and printID in jsondata:
                    customerID = jsondata[printID]
                else:
                    self.write("Print ID {0} is not a valid customer ID.".format(printID))
                    return
                self.set_cookie("digitATM", customerID)
        with open("menu.html", "r") as htmlfile:
            data = htmlfile.read().replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

class BalanceHandler(tornado.web.RequestHandler):
    def get(self):
        customerID = self.get_cookie("digitATM")
        if customerID is not None:
            balance = RequestManager.getBalance(customerID)
        else:
            self.write("An error occurred when attempting to get the hash value for this customer.".format(customerID))
            return
        if balance is not None:
            self.write("Customer ID: {0}\nBalance: {1}".format(customerID, balance))
            return
        self.write("Customer ID {0} and its corresponding hash exist. However, the balance for this customer could not be determined.".format(customerID))         

class WithdrawHandler(tornado.web.RequestHandler):
    def post(self):
        customerID = self.get_cookie("digitATM")
        amount = self.get_argument("amount", "")
        if customerID is not None:
            RequestManager.withdraw(customerID, amount)
            self.write("Withdrew {0} from customer ID {1}'s account.".format(locale.currency(float(amount), grouping=True), customerID))
        else:
            self.write("Although customer ID {0} exists, an error occurred when attempting to get the hash value for customer ID {0}.".format(customerID))
            return

class DepositHandler(tornado.web.RequestHandler):
    def post(self):
        customerID = self.get_cookie("digitATM")
        amount = self.get_argument("amount", "")
        if customerID is not None:
            RequestManager.withdraw(customerID, amount)
            self.write("Deposited {0} in customer ID {1}'s account.".format(locale.currency(float(amount), grouping=True), customerID))
        else:
            self.write("Although customer ID {0} exists, an error occurred when attempting to get the hash value for customer ID {0}.".format(customerID))
            return

class StyleHandler(tornado.web.RequestHandler):
    def get(self):
        data = None
        with open("styles.css", "r") as htmlfile:
            data = htmlfile.read() #.replace("\n", "")
        data = data if data is not None else ERROR_MESSAGE
        self.write(data)

def my_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/menu", MenuHandler),
        (r"/debug", DebugHandler),
        (r"/tryagain", TryAgainHandler),
        (r"/nomatch", NoMatchHandler),
        (r"/balance", BalanceHandler),
        (r"/withdraw", WithdrawHandler),
        (r"/deposit", DepositHandler),
        (r"/styles.css", StyleHandler),
    ])

if __name__ == "__main__":
    locale.setlocale( locale.LC_ALL, '' )
    app = my_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
