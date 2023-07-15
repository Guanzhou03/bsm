from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class MyWrapper(EWrapper):
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("Contract Details:")
        print(f"  Request ID: {reqId}")
        print(f"  Symbol: {contractDetails.contract.symbol}")
        print(f"  Expiry: {contractDetails.contract.lastTradeDateOrContractMonth}")
        print(f"  Strike: {contractDetails.contract.strike}")
        print(f"  Right: {contractDetails.contract.right}")
        print(f"  Exchange: {contractDetails.contract.exchange}")
        print(f"  Currency: {contractDetails.contract.currency}")
        print("HERE")

class MyClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
    def run(self):
        self.wrapper.run()
    

wrapper = MyWrapper()
client = MyClient(wrapper)
client.connect("127.0.0.1", 7497, 0)
