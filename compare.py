#!/usr/bin/env python3
##################################
#                                #
#                                #
#      Created by Kevin Luo      #
#                                #
#                                #
##################################

# v1 (COMPLETE): Pulls from 3 different sites and compares prices differences of ETH-BTC, returns lowest and highest values and returns artitrage price and amount of ETH needed to profit 0.01 BTC

# v2(INCOMPLETE): Continiously pull from sites and compare prices, do not return unless artitrage returns is > threhold

# v3(INCOMPLETE): Pull from different BTC-COINS from different sites and return one with highest artitrage

# usage: ./compare.py



import urllib.request
import json
import re
from decimal import getcontext, Decimal


def main():
    getcontext().prec = 3

    ir_trading_fee = 0.5 #percentagae
    btcm_trading_fee = 0.85 #percentage

    ir_withdrawl_fee = 0.0001 #btc, free with api
    btcm_withdrawl_fee = 0.0001 #btc

    amount_2_profit = 0

    binance_url = "https://api.binance.com/api/v1/ticker/24hr?symbol=ETHBTC"
    btcm_url = "https://api.btcmarkets.net/market/ETH/BTC/tick"
    bittrex_url = "https://bittrex.com/Api/v2.0/pub/market/GetLatestTick?marketName=BTC-ETH&tickInterval=oneMin"


    s1 = float(get_lastprice_api_request(binance_url, "lastPrice"))
    s2 = float(get_lastprice_api_request(btcm_url, "lastPrice"))
    s3 = float(get_lastprice_api_request_multi(bittrex_url,"result",0,"L"))

    print ("Binance:                " + str(s1))
    print ("IndependantReserve:     " + str(s2))
    print ("Bittrex:                " + str(s3))

    threshold_var = 0.01 # ~> $50USD

    max_value = max({s1, s2, s3})
    min_value = min({s1, s2, s3})
    if max == min:
        print("FAIL")

    if max_value == s1:
        highest_exchange = "Binance"
    elif max_value == s2:
        highest_exchange = "BTC_M"
    elif max_value == s3:
        highest_exchange = "Bittrex"

    if min_value == s1:
        lowest_exchange = "Binance"
    elif min_value == s2:
        lowest_exchange = "BTC_M"
    elif min_value == s3:
        lowest_exchange = "Bittrex"
    # print("max:" + str(max_value))
    # print("min:" + str(min_value))


    diff = percentageDifference(max_value, min_value)
    amount_2_profit = threshold_var / (max_value-min_value)
    print("Arbitrage:              " + str(diff) + "%    :" + lowest_exchange + " -> " + highest_exchange)

    print("Cost to make 0.01BTC:   ETH:" + str(amount_2_profit) + " == $" + str(amount_2_profit * 500)) #avg price of eth at 19/6/18


def percentageDifference(v1, v2):
    # Set the precision.
    getcontext().prec = 3
    value1 = abs(v1-v2)
    value2 = (v1+v2)/2
    value3 = (Decimal(value1)/Decimal(value2)) * 100
    return (value3)

def get_lastprice_api_request(url, json_format):
    req = urllib.request.urlopen(url).read()
    json_fields = json.loads(req)
    return json_fields[json_format]

def get_lastprice_api_request_multi(url, json_format, json_format1, json_format2):
    req = urllib.request.urlopen(url).read()
    json_fields = json.loads(req)
    return json_fields[json_format][json_format1][json_format2]


if __name__ == '__main__':
    main()
