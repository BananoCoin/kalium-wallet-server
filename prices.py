import redis, urllib3, certifi, socket, json, time, os, sys
from coinmarketcap import Market

#rblocks = redis.StrictRedis(host='localhost', port=6379, db=0)
#rwork = redis.StrictRedis(host='localhost', port=6379, db=1)
rdata = redis.StrictRedis(host='localhost', port=6379, db=2)

currency_list = [ "AUD", "BRL", "BTC", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NANO", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR" ]

def creeper():
	try:
		cmc = Market(base_url='https://api.creeper.banano.cc/')
		for currency in currency_list:
			try:
				price_data = cmc.ticker(convert=currency.upper())
				data_name = currency.upper()
				price_currency = price_data['data']['quotes'][data_name]['price']
				print(rdata.hset("prices", "creeper:banano-"+currency.lower(), price_currency),"Creeper BANANO-"+currency.upper(), price_currency)
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print('exception',exc_type, exc_obj, exc_tb.tb_lineno)
				print("Failed to get price for BANANO-"+currency.upper()+" Error")
		print(rdata.hset("prices", "creeper:lastupdate",int(time.time())),int(time.time()))
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print('exception',exc_type, exc_obj, exc_tb.tb_lineno)
		print("Failed to load from Creeper")

creeper()

print("Creeper BANANO-USD:", rdata.hget("prices", "creeper:banano-usd").decode('utf-8'))
print("Creeper BANANO-NANO:", rdata.hget("prices", "creeper:banano-nano").decode('utf-8'))
print("Creeper BANANO-BTC:", rdata.hget("prices", "creeper:banano-btc").decode('utf-8'))
print("Last Update:          ", rdata.hget("prices", "creeper:lastupdate").decode('utf-8'))

