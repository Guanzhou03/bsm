from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import time
import threading

class MyWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self.contract_id = None

    def reqContractDetails(self, reqId, contract):
        super().reqContractDetails(reqId, contract)
        print("Requesting contract details for {}...".format(contract.symbol))

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)

class IBApi(EWrapper, EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

class Bot:
    def __init__(self):
        self.ib = IBApi(MyWrapper())
        self.ib.connect("127.0.0.1", 7497, 1)
        time.sleep(3)
        self.ib.reqIds(-1)
        ib_thread = threading.Thread(target= self.runLoop, daemon=True)
        ib_thread.start()

    def placeOrder(self, contract, order):
        self.ib.placeOrder(1, contract, order)
    
    def runLoop(self):
        self.ib.run()

# Create a new contract object for the AAPL call option
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20240621"
contract.strike = 150
contract.right = "C"

# Define the order for the option contract
order = Order()
order.action = "BUY"
order.totalQuantity = 1
order.orderType = "LMT"
order.lmtPrice = 10.0
order.eTradeOnly = False
order.firmQuoteOnly = False

print("Creating bot...")
client = Bot()
# Request contract details for the option contract
time.sleep(3)
client.ib.reqContractDetails(1, contract)

# Place order for the option contract
client.placeOrder(contract, order)

# Wait for the order to be filled or cancelled
time.sleep(10)

# Disconnect from the IB API
client.ib.disconnect()