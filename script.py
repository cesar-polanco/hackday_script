#!/usr/bin/python3

import urllib.request
import json

URL_PREFIX = 'http://'
URL_POSTFIX = '/computer/api/json'
MASTER_COUNT = {'test': 1}# Dictionary mapping master series entry with count for that master series
MASTER_SERIES_LIST = ['test'] # List object containing all master series to be tested

def append_user_to_slave_info(slave_info, master_series, master_number):
    asi = {'name': slave_info['name']}
    reason_string = slave_info['offline_reason']
    url = URL_PREFIX + master_series + '-' + str(master_number) + '/computer/' + slave_info['name']
    with urllib.request.urlopen(url) as req:
        html_slave_page = req.read().decode('UTF-8')
        for html_piece in html_slave_page.split('</p>'):
            if '<p class="warning">' in html_piece:
                reason_string ='taken offline by ' + html_piece[html_piece.find('<p class="warning">') + len('<p class="warning">Disconnected by'):]
    if reason_string != '':
        asi['offline_reason'] = reason_string
    else:
        asi['offline_reason'] = 'Unknown reason'
    return asi

def curl_jenkins(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read()

def get_slave_information(slave):
    formatted_slave = { 'name': slave['displayName'] }
    if 'No route to host' in slave['offlineCauseReason']:
        formatted_slave['offline_reason'] = 'No Route to Host'
    else:
        formatted_slave['offline_reason'] = slave['offlineCauseReason']
    return formatted_slave

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
                        slave_info = get_slave_information(json_output['computer'][y+1])
                        slave_info = append_user_to_slave_info(slave_info, master_series, x+1)
                        offline_slaves.append(slave_info)
            print_slave_results(offline_slaves, master_series, x+1)

def print_slave_results(offline_slave_list, master_series, master_number):
    if len(offline_slave_list) < 1:
        print('No offline slaves for ' + master_series + '-' + str(master_number))
    else:
        print('There are ' + str(len(offline_slave_list)) + ' offline slaves for ' + master_series + '-' + str(master_number) + ":")
        for slave in offline_slave_list:
            print('\t' + slave['name'] + ' is currently offline due to: ' + slave['offline_reason'])

if __name__ == "__main__":
    check_on_jenkins_slaves()