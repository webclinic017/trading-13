import os
import sys
import requests
import json


class apiUtils:
    def __init__(self):
        pass


    def get_last_bar(self, scrip_name):
        url = "https://history.truedata.in/getlastnbars?symbol=" + scrip_name + "&response=csv&nbars=1&interval=1min&bidask=1"

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #print(response.text)
        return response.text

    def authenticate(self):
        url = "https://auth.truedata.in/token"
        payload = 'username=tdws114&password=suraj%40114&grant_type=password'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        #print(response.text)
        json_response = json.loads(response.text)

        #print(type(json_response))
        #print(json_response["access_token"])
        self.token = json_response["access_token"]

