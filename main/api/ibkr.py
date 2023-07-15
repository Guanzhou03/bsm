from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import time

class MyWrapper(EWrapper):
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("Contract Details for Request ID {}:".format(reqId))
        print(contractDetails)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)

class MyClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

# Define the contract for which you want option data
order = Order()
order.action = "BUY"
order.totalQuantity = 1
order.orderType = "LMT"
order.lmtPrice = 10.0

# Create a new contract object for the AAPL call option
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20240621"
contract.strike = 150
contract.right = "C"

# Create instances of the client and wrapper classes
wrapper = MyWrapper()
client = MyClient(wrapper)

# Connect to the TWS or IB Gateway application
client.connect("127.0.0.1", 7497, 0)
time.sleep(3)

# Request contract details for the option contract
client.reqContractDetails(1, contract)

client.reqAccountUpdates(True, "DU001") # Replace with your paper trading account number
client.reqIds(-1)
# Start the event loop to receive responses from the TWS API
client.run()
# Place the order
client.placeOrder(1, contract, order)
print("Client is connected:", client.isConnected())