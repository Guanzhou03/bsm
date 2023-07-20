from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.ticktype import TickTypeEnum
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
    
    def tickOptionComputation(self, reqId, tickType, tickAttrib: int,
                                   impliedVol: float, delta: float, optPrice: float, pvDividend: float,
                                   gamma: float, vega: float, theta: float, undPrice: float):
             super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta,
                                           optPrice, pvDividend, gamma, vega, theta, undPrice)
             print("TickOptionComputation. TickerId:", reqId, "TickType:", tickType,
                   "TickAttrib:", tickAttrib,
                   "ImpliedVolatility:", impliedVol, "Delta:", delta, "OptionPrice:",
                   optPrice, "pvDividend:", pvDividend, "Gamma: ", gamma, "Vega:", vega,
                  "Theta:", theta, "UnderlyingPrice:", undPrice)

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
        self.ib.placeOrder(2, contract, order)
    
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


def create_order(action, qty, type, limit_price):
    order = Order()
    order.action = action
    order.totalQuantity = qty
    order.orderType = type
    order.lmtPrice = limit_price
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order
    
order = create_order("BUY", 1, "LMT", 20)
print("Creating bot...")
client = Bot()
# Request contract details for the option contract
# client.ib.reqContractDetails(2, contract)
# client.ib.reqMarketDataType(3)
# client.ib.reqMktData(4, contract, "", False, False, None)
# Place order for the option contract
client.placeOrder(contract, order)

# Wait for the order to be filled or cancelled
time.sleep(10)

# Disconnect from the IB API
client.ib.disconnect()