from random import choice, randrange
import string
import requests
import json


def ip_generator():
    return str(".".join([str(randrange(0, 255)),
                         str(randrange(0, 255)),
                         str(randrange(0, 255)),
                         str(randrange(1, 255))]))


def pwd_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(choice(chars) for x in range(size))


def generate_num_account():
    chars = string.digits
    account = ''.join(choice(chars) for x in range(10))
    return account

def generate_account(len_acc=64):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    account = ''.join(choice(chars) for x in range(len_acc))
    return account

def generate_pw(len_pw=64):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    pw = ''.join(choice(chars) for x in range(len_pw))
    return pw

def get_btc_value():
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    get_data = requests.get(key)
    data = get_data.json()
    current_value = float(data['price'])
    print(type(current_value))
    return data['price']
