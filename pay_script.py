
from cloudipsp import Api, Checkout
import requests
from cloudipsp import Order


def create_pay(ID, SUMM):
	api = Api(merchant_id=1472036, secret_key='4C0lTKN0Kesm4G9YJjycknAgRXZhaGAr')
	checkout = Checkout(api=api)
	data = {
		'order_id': ID,
	    "amount": SUMM,
	    "order_desc":"help",
	    "currency": "UAH",
	    "merchant_id": '1472036',
	    "response_url": 'https://t.me/KymAvtoBot',
	    "lifetime": 600
	}

	url = checkout.url(data)
	return url['checkout_url']

def check(ID):
	api = Api(merchant_id=1472036, secret_key='4C0lTKN0Kesm4G9YJjycknAgRXZhaGAr')
	ordd = Order(api=api)
	st = ordd.status({'order_id': ID})
	print(st)	
	return st['order_status']

 
print(create_pay(444,100))
print(check(444))