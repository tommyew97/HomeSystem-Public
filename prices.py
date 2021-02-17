import cryptocompare

class Prices():
    def __init__(self):
        self.bitcoin_init = 9200
        self.dogecoin_init = 0.024
        self.litecoin_init = 177

    def get_bitcoin_price(self):
        price = cryptocompare.get_price('BTC', curr='USD')['BTC']['USD']
        formated = str(price)[0:2] + " " + str(price)[2::] + "$"
        returns = self.calculate_return(self.bitcoin_init, price)
        return [formated, returns]

    def get_dogecoin_price(self):
        price = cryptocompare.get_price("DOGE", curr='USD')['DOGE']['USD']
        formated = str(price) + "$"
        returns = self.calculate_return(self.dogecoin_init, price)
        return [formated, returns]

    def get_litecoin_price(self):
        price = cryptocompare.get_price("LTC", curr='USD')['LTC']['USD']
        formated = str(price) + "$"
        returns = self.calculate_return(self.litecoin_init, price)
        return [formated, returns]

    def calculate_return(self, init, current):
        curr_return = ((current/init) - 1)*100
        curr_return_str = ("{returns:.2f}%").format(returns=curr_return)
        return curr_return_str