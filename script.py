#!/usr/bin/python3

import urllib.request
import json

URL_PREFIX = 'http://'
URL_POSTFIX = '/computer/api/json'
MASTER_COUNT = {'test':1}# Dictionary mapping master series entry with count for that master series 
MASTER_SERIES_LIST = ['test'] # List object containing all master series to be tested

def curl_jenkins(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read()

def get_slave_information(slave):


def check_on_jenkins_slaves():
    for master_series in MASTER_SERIES_LIST:
        for x in range(MASTER_COUNT[master_series]):
            offline_slaves = []
            combined_url = URL_PREFIX + master_series + '-' + str(x+1) + URL_POSTFIX
            curl_response = curl_jenkins(combined_url)
            json_output = json.loads(curl_response.decode('UTF-8'))
            if json_output is not None:
                slave_count = len(json_output['computer'])
                for y in range(slave_count - 1):
                    offline = json_output['computer'][y+1]['offline']
                    if offline:
                        offline_slaves.append(json_output['computer'][y+1]['displayName'])

            print_slave_results(offline_slaves, master_series, x+1)

def print_slave_results(offline_slave_list, master_series, master_number):
    if len(offline_slave_list) < 1:
        print('No offline slaves for ' + master_series + '-' + str(master_number))
    else:
        print('Offline slaves exist for ' + master_series + '-' + str(master_number))

if __name__ == "__main__":
    check_on_jenkins_slaves()