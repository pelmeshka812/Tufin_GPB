# Input should be like the line below passed as src_dst_list
# [['Администраторы Linux', [['ex1105', '172.16.200.15', 'none'], ['ex0105', '172.16.200.230', 'none'], ['ex0105', '172.16.200.128', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '443'], ['TCP', 443]], 'TCP\nHTTPS', 'Тестовый комментарий третий'], ['Прикладные администраторы', [['gpbu0105', '10.3.3.211', 'none'], ['gpbu0106', '10.3.3.119', 'none'], ['gpbu0107', '10.3.3.14', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '445'], ['TCP', 443], ['TCP', 22]], 'TCP\nHTTPS\nSSH', 'Тестовый комментарий первый']]
import sys
import subprocess
import socket
import json
import requests
import ipaddress
import io
import pandas as pd
import base64
import sqlite3
import time
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# src_dst_list = [['Администраторы Linux', [['ex1105', '172.16.200.15', 'none'], ['ex0105', '172.16.200.230', 'none'], ['ex0105', '172.16.200.128', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '443'], ['TCP', 443]], 'TCP\nHTTPS', 'Тестовый комментарий третий'], ['Прикладные администраторы', [['gpbu0105', '10.3.3.211', 'none'], ['gpbu0106', '10.3.3.119', 'none'], ['gpbu0107', '10.3.3.14', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '445'], ['TCP', 443], ['TCP', 22]], 'TCP\nHTTPS\nSSH', 'Тестовый комментарий первый']]

def validate_addresses(src_dst_item):
    for item in src_dst_item[1]:
        try:
            socket.inet_aton(item[1])
        except socket.error:
            print('IP not validated')
            return False
    for item in src_dst_item[2]:
        try:
            socket.inet_aton(item[0])
        except socket.error:
            print('IP not validated')
            return False
    return True


def main(src_dst_list):
    # API Server
    server_address = 'https://10.1.101.210/securetrack/api/'
    tufin_api_user = 'admin'
    tufin_api_password = '1q2w3e'

    # Get Unified Security Policy in Data Frame
    get_usp_url = server_address + 'security_policies/3/export'
    get_usp_headers = {'Content-type': 'application/json'}
    resp_get_usp = requests.get(get_usp_url, headers=get_usp_headers, auth=(
        tufin_api_user, tufin_api_password), verify=False).content
    response_get_usp_df = pd.read_csv(io.BytesIO(resp_get_usp), delimiter=',')

    # Get all zone names and id's in Data Frame
    print('Loading zone info')
    all_zone_ids = []
    all_zone_names = []
    get_zones_url = server_address + 'zones/'
    zone_headers = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
    resp_zones = requests.get(get_zones_url, headers=zone_headers, auth=(
        tufin_api_user, tufin_api_password), verify=False)
    response_zones = json.loads(resp_zones.content)
    response_zones = response_zones['zones']['zone']
    for res in response_zones:
        all_zone_ids.append(res['id'])
        all_zone_names.append(res['name'])
    zone_details_df = pd.DataFrame(
        {'id': all_zone_ids, 'name': all_zone_names})

    # Get networks for all zones into a Data Frame
    get_zone_entries_df = pd.DataFrame(
        columns=['id', 'name', 'entry_id', 'network', 'netmask', 'prefix', 'domain'])
    for index, row in zone_details_df.iterrows():
        get_zone_entries_url = server_address + \
                               'zones/' + row['id'] + '/entries'
        zone_entries_headers = {
            'Content-type': 'application/json', 'Accept': 'application/json'}
        resp_zones_entries = requests.get(get_zone_entries_url, headers=zone_entries_headers, auth=(
            tufin_api_user, tufin_api_password), verify=False).content
        response_zone_entries = json.loads(resp_zones_entries)
        if response_zone_entries['zone_entries']['total'] > 0:
            for entry in response_zone_entries['zone_entries']['zone_entry']:
                ipv4_interface = ipaddress.IPv4Interface(entry['ip'] + '/24')
                ipv4_network = ipv4_interface.network
                new_entry = {'id': entry['zoneId'], 'name': entry['zoneName'], 'entry_id': entry['id'],
                             'network': ipv4_network, 'netmask': entry['netmask'], 'prefix': entry['prefix'],
                             'domain': entry['domain']}
                get_zone_entries_df = get_zone_entries_df.append(
                    new_entry, ignore_index=True)

    # Data Frame with zones and deatils
    zone_entry_details_df = get_zone_entries_df.merge(zone_details_df, on='name', how='right').drop(
        ['id_x'], axis=1)
    zone_entry_details_df.rename(columns={
        'id_y': 'id'}, inplace=True)

    # Iterating throgh requests one by one
    # Each item is one request (1 line from the excel file)
    # Adding to list of src/dst ips and networks
    counter = 1
    src_dst_passed = []
    for src_dst_item in src_dst_list:
        print('processing item --- ' + str(src_dst_item))
        counter = counter + 1
        valid_ips = validate_addresses(src_dst_item)
        if valid_ips == False:
            continue
        else:
            access_role_list = []
            if len(src_dst_item[1]) == 3:
                for element in src_dst_item[1]:
                    access_role_list.append(
                        element[2] + '_' + element[1] + '_24')
            device_list = []
            src_ip_addresses = []
            src_networks = []
            src_address = ''
            src_adr_mask_list = []
            dst_ip_addresses = []
            dst_address = ''
            dst_networks = []
            dst_adr_mask_list = []
            src_zone = ''
            dst_zone = ''
            for i in src_dst_item[1]:
                src_netmask = []
                dst_netmask = []
                if i[1] != 'none':
                    src_address = ipaddress.IPv4Interface(i[1] + '/24')
                    src_networks.append(src_address.network)
                    src_netmask.append(str(src_address)[:-3])
                    src_netmask.append('255.255.255.255')
                    src_ip_addresses.append(i[1])
                else:
                    src_address = ipaddress.IPv4Interface(i[0] + '/24')
                    src_networks.append(src_address.network)
                    src_netmask.append(str(src_address)[:-3])
                    src_netmask.append('255.255.255.255')
                    src_ip_addresses.append(i[0])
                src_adr_mask_list.append(src_netmask)
            for i in src_dst_item[2]:
                dst_netmask = []
                if i[1] != 'none':
                    dst_address = ipaddress.IPv4Interface(i[1] + '/24')
                    dst_networks.append(dst_address.network)
                    dst_netmask.append(str(dst_address)[:-3])
                    dst_netmask.append('255.255.255.255')
                    dst_ip_addresses.append(i[1])
                else:
                    dst_address = ipaddress.IPv4Interface(i[0] + '/24')
                    dst_networks.append(dst_address.network)
                    dst_netmask.append(str(dst_address)[:-3])
                    dst_netmask.append('255.255.255.255')
                    dst_ip_addresses.append(i[0])
                dst_adr_mask_list.append(dst_netmask)

                # Checking source & destination zones (in zones & USP zones)
            print('Checking source & destination zones (in zones & USP zones)')
            for src_net in src_networks:
                src_zone_entry = zone_entry_details_df[(
                        zone_entry_details_df['network'] == src_net)].values.tolist()
                if len(src_zone_entry) > 0:
                    for usp_zone_check in src_zone_entry:
                        if len(response_get_usp_df[
                                   (response_get_usp_df['from zone'] == usp_zone_check[0])].values.tolist()) > 0:
                            src_zone = usp_zone_check[0]

            for dst_net in dst_networks:
                dst_zone_entry = zone_entry_details_df[(
                        zone_entry_details_df['network'] == dst_net)].values.tolist()
                if len(dst_zone_entry) > 0:
                    for usp_zone_check in dst_zone_entry:
                        if len(response_get_usp_df[
                                   (response_get_usp_df['to zone'] == usp_zone_check[0])].values.tolist()) > 0:
                            dst_zone = usp_zone_check[0]

            if src_zone == '':
                print('Some source addresses not found')
            if dst_zone == '':
                print('Some destination addresses not found')

                # Checking USP rules
            print('Checking USP rules')
            if src_zone != '' and dst_zone != '':
                requested_ports = src_dst_item[4].split('\n')
                if 'TCP' in requested_ports:
                    requested_ports.remove('TCP')
                matrix_intersection_pre_row = response_get_usp_df[(response_get_usp_df['from zone'] == src_zone) & (
                        response_get_usp_df['to zone'] == dst_zone)].values.tolist()
                matrix_intersection_row = matrix_intersection_pre_row[0]
                proceed = ''
                if matrix_intersection_row[3] == 'block all':
                    print('USP --- Block All')
                    break
                elif matrix_intersection_row[3] == 'block only':
                    blocked_services_list = matrix_intersection_row[4].split(
                        ';')
                    for port_i in requested_ports:
                        if port_i.lower() in blocked_services_list:
                            print('USP --- Block Only')
                            break
                        else:
                            src_dst_passed.append(src_dst_item)
                elif matrix_intersection_row[3] == 'allow only':
                    allowed_services = matrix_intersection_row[4].split(';')
                    allowed_services_list = [item.lower()
                                             for item in allowed_services]
                    for port_i in requested_ports:
                        if port_i.lower() in allowed_services_list:
                            proceed = 'Y'
                        else:
                            print('USP --- Allow Only')
                            proceed = 'N'
                            break
                    if proceed == 'Y':
                        src_dst_passed.append(src_dst_item)
                elif matrix_intersection_row[3] == 'allow all':
                    src_dst_passed.append(src_dst_item)
    return src_ip_addresses, dst_ip_addresses, src_dst_passed, access_role_list


passed_result = main(request)
