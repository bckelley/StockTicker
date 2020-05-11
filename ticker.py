import os, sys, time
import urllib3
import re, json
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup

def ticker():
    try:
        symbols = ['PINS','AAPL','BYND','SNAP']
        table = PrettyTable()
        table.field_names = ['Symbol',  'Company Name', 'Price',    'Net Change',   'Percentage Change',    'Indicator']
        for symbol in symbols:
            link = "https://api.nasdaq.com/api/quote/%s/info?assetclass=stocks"%(symbol)
            
            response = requests.get(link)
            data = json.loads(response.text)
            
            status = data['data']['marketStatus']
            symbol = data['data']['symbol']
            name = data['data']['companyName']
            if status == "Market Open":
                price = data['data']['primaryData']['lastSalePrice']
                netChange = data['data']['primaryData']['netChange']
                perChange = data['data']['primaryData']['percentageChange']
                timestamp = data['data']['primaryData']['lastTradeTimestamp']
            elif status == "After Hours":
                price = data['data']['secondaryData']['lastSalePrice']
                netChange = data['data']['secondaryData']['netChange']
                perChange = data['data']['secondaryData']['percentageChange']
                timestamp = data['data']['secondaryData']['lastTradeTimestamp']
            delta = data['data']['primaryData']['deltaIndicator']
            
            table.add_row([symbol,  name,   price,  netChange,  perChange,  delta])

        funds = ['AGG', 'SPGM']
        for fund in funds:
            link = "https://api.nasdaq.com/api/quote/%s/info?assetclass=etf"%(fund)

            response = requests.get(link)
            data = json.loads(response.text)
            
            symbol = data['data']['symbol']
            name = data['data']['companyName']
            price = data['data']['primaryData']['lastSalePrice']
            netChange = data['data']['primaryData']['netChange']
            perChange = data['data']['primaryData']['percentageChange']
            delta = data['data']['primaryData']['deltaIndicator']
            status = data['data']['marketStatus']
            
            table.add_row([symbol,  name,   price,  netChange,  perChange,  delta])
        print(table)

        if status == "Market Open":
            print("Open %s"%(timestamp))
            time.sleep(300)
        elif status == "After Hours":
            print("After Hours %s"%(timestamp))
            time.sleep(300)
        else:
            print("The Markets are currently Closed.")
            time.sleep(57600)
        
    except Exception as e:
        print("Failed to process the request, Exception: %s "%(e))

if __name__ == "__main__":
    while True:
        ticker()
