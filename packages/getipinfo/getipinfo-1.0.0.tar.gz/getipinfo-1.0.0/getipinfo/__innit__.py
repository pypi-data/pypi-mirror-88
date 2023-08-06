import requests
import json

resp = requests.get('https://ipinfo.io/json', verify = True)

if resp.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()
data = resp.json()

def getip():
    return data['ip']

def getcity():
    return data['city']

def getregion():
    return data['region']

def getcountry():
    return data['country']

def getlocation():
    return data['loc']

def getpostalcode():
    return data['postal']

def gettimezone():
    return data['timezone'] 