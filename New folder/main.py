import prase_excel
import subprocess
import socket
import json
import requests
import ipaddress
import io
import pandas as pd
#import credentials
import base64
#import checkpoint_add_new_rule
import sqlite3

import time
import urllib3
import datetime
#import _access_role_methods

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
this_id = 'id_41'


def check_path(src_ip_addresses, dst_ip_addresses, src, dst, src_dst_item, jid, access_role_list):
    conn = createConnection()
    tufin_api_user = 'admin'
    tufin_api_password = base64.b85decode(
        config.tufin_password()).decode("utf-8")
    srvc = []
    services = src_dst_item[4]
    services_list = services.split('\n')
    if 'TCP' in services_list: services_list.remove('TCP')
    if 'UDP' in services_list: services_list.remove('UDP')
    if 'TCP, UDP' in services_list: services_list.remove('TCP, UDP')
    for services in src_dst_item[3]:
        pre_srvc = []
        pre_srvc.append(str(services[1]))
        pre_srvc.append(services[0])
        srvc.append(pre_srvc)
    for source in src_ip_addresses:
        for destination in dst_ip_addresses:
            # tufin_url = 'https://10.1.101.210/securetrack/api/topology/path?src=172.16.2.1/24&dst=10.1.104.1/24&service=tcp:80'
            tufin_url = 'https://10.1.101.210/securetrack/api/topology/path?src=' + \
                        str(source) + '/24&dst=' + str(destination) + \
                        '/24&service=any'
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}
            resp = requests.get(tufin_url, headers=headers, auth=(
                tufin_api_user, tufin_api_password), verify=False)
            response = json.loads(resp.content)
            if len(response['path_calc_results']['device_info']) > 0:
                for dvc_info in response['path_calc_results']['device_info']:
                    device_name = dvc_info['name'].strip("'")
                    if dvc_info['vendor'] == "Generic":
                        cmd_src_dst_item = src_dst_item
                        for items in cmd_src_dst_item[1]:
                            if len(items) > 2:
                                items.remove(items[2])
                        cmd_src_dst_item.remove(cmd_src_dst_item[4])
                        nsx_cmd = str(cmd_src_dst_item)
                        nsx_cmd = 'pwsh testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' + nsx_cmd + '"'  # For Linix
                        # nsx_cmd = 'powershell.exe testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' # For Windows
                        # pscommand = 'testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' # For Windows
                        # nsx_resp = subprocess.Popen(['powershell.exe', '-NoProfile', '-Command', '"&{' + pscommand + '}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        nsx_resp = subprocess.run(nsx_cmd, shell=True, stdout=subprocess.PIPE)
                        # sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                        # jid+"', 'Generic Device response = '"+ str(nsx_resp) + "', '"+config.now()+"' )"
                        # cur = conn.cursor()
                        # cur.execute(sql)
                        # conn.commit()
                        tufin_all_url = 'https://10.1.101.210/securetrack/api/devices/'
                        headers_id = {'Content-type': 'application/json',
                                      'Accept': 'application/json'}
                        resp_devices = requests.get(tufin_all_url, headers=headers_id, auth=(
                            tufin_api_user, tufin_api_password), verify=False)
                        response_devices = json.loads(resp_devices.content)
                        for device_resp in response_devices['devices']['device']:
                            if device_resp['name'] == dvc_info['name']:
                                sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                                      jid + "', 'Generic Device ip address  = '" + device_resp[
                                          'ip'] + "', '" + config.now() + "' )"
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                    elif dvc_info['vendor'] == "Check Point":
                        device_list_gw = []
                        device_list_mgmt = []
                        pre_pre_device_list = []
                        tufin_id_url = 'https://10.1.101.210/securetrack/api/devices/' + \
                                       str(dvc_info['id'])
                        headers_id = {'Content-type': 'application/json',
                                      'Accept': 'application/json'}
                        resp = requests.get(tufin_id_url, headers=headers_id, auth=(
                            tufin_api_user, tufin_api_password), verify=False)
                        response_id = json.loads(resp.content)
                        tufin_parent_id_url = 'https://10.1.101.210/securetrack/api/devices/' + \
                                              str(response_id['device']['parent_id'])
                        resp_parent = requests.get(tufin_parent_id_url, headers=headers_id, auth=(
                            tufin_api_user, tufin_api_password), verify=False)
                        response_parent_id = json.loads(resp_parent.content)
                        mgmt_ip = str(response_parent_id['device']['ip'])
                        if mgmt_ip == '10.1.101.53':
                            if len(access_role_list) > 0:
                                print('1')
                                for access_role in access_role_list:
                                    network_ip = access_role.split("_")
                                    params = dict()
                                    params['networks'] = 'new_host_tufin_' + network_ip[1]
                                    chkpnt_addrole_resp = _access_role_methods.add_access_role(mgmt_ip, tufin_api_user,
                                                                                               tufin_api_password,
                                                                                               access_role, **params)
                                    print(chkpnt_addrole_resp)

                                chkpnt_addrule_resp = checkpoint_add_new_rule.add_new_rule(mgmt_ip, dvc_info['name'],
                                                                                           access_role_list, None,
                                                                                           dst_ip_addresses,
                                                                                           services_list, None)
                                if chkpnt_addrule_resp == True:
                                    sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                                          jid + "', 'The changes were published successfully on " + device_name + "', '" + config.now() + "' )"
                                else:
                                    sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                                          jid + "', 'Failed to publish successfully on " + device_name + "', '" + config.now() + "' )"
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                            else:
                                checkpoint_resp = checkpoint_add_new_rule.add_new_rule(
                                    mgmt_ip, dvc_info['name'], None, src_ip_addresses, dst_ip_addresses, services_list,
                                    None)
                                print(checkpoint_resp)
                                if chkpnt_addrule_resp == True:
                                    sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                                          "', 'The changes were published successfully on " + \
                                          device_name + "', '" + \
                                          config.now() + "' )"
                                else:
                                    sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                                          "', 'Failed to publish successfully on " + \
                                          device_name + "', '" + \
                                          config.now() + "' )"
                                cur = conn.cursor()
                                cur.execute(sql)
                                conn.commit()
                        else:
                            checkpoint_resp = checkpoint_add_new_rule.add_new_rule(mgmt_ip, dvc_info['name'], None,
                                                                                   src_ip_addresses, dst_ip_addresses,
                                                                                   services_list, None)
                            if chkpnt_addrule_resp == True:
                                sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                                      "', 'The changes were published successfully on " + \
                                      dvc_info['name'] + "', '" + \
                                      config.now() + "' )"
                            else:
                                sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                                      jid + "', 'Failed to publish successfully on " + \
                                      dvc_info['name'] + \
                                      "', '" + config.now() + "' )"
                            cur = conn.cursor()
                            cur.execute(sql)
                            conn.commit()
                            print(checkpoint_resp)
                            # print(mgmt_ip)
                            # print(src)
                            # print(dst)
                            # print(srvc)
                            # print(response_id['device']['ip'])  # Gateway
                            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                                  jid + "', 'calling checkpoint management " + mgmt_ip + "', '" + config.now() + "' )"
                            cur = conn.cursor()
                            cur.execute(sql)
                            conn.commit()
                        # main_searches(mgmt_ip, src, dst, srvc, response_id['device']['ip'])
                        # sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                        #     jid+"', 'Processing request, please wait ...', '"+config.now()+"' )"
                        # cur = conn.cursor()
                        # cur.execute(sql)
                        # conn.commit()                            
                break
            break
        break


def validate_addresses(src_dst_item, jid):
    conn = createConnection()
    for item in src_dst_item[1]:
        try:
            socket.inet_aton(item[1])
        except socket.error:
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + "', 'Invalid IP " + item[
                1] + "', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return False
    for item in src_dst_item[2]:
        try:
            socket.inet_aton(item[0])
        except socket.error:
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + "', 'Invalid IP " + item[
                0] + "', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return False
    return True




def main(jid):
    # conn = createConnection()
    # sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
    # jid + "', ' Processing Request ', '" + config.now() + "' )"
    # cur = conn.cursor()
    # cur.execute(sql)
    # conn.commit()
    # API Server
    server_address = 'https://10.1.101.210/securetrack/api/'
    # tufin_api_user = 'admin'
    # tufin_api_password = base64.b85decode(
    # config.tufin_password()).decode("utf-8")

    # Get data from excel file
    src_dst_list = prase_excel.parse_excel()

    # Get Unified Security Policy in Data Frame
    get_usp_url = server_address + 'security_policies/3/export'
    get_usp_headers = {'Content-type': 'application/json'}
    resp_get_usp = requests.get(get_usp_url, headers=get_usp_headers, auth=(
        tufin_api_user, tufin_api_password), verify=False).content
    response_get_usp_df = pd.read_csv(io.BytesIO(resp_get_usp), delimiter=',')

    # Get all zone names and id's in Data Frame

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
    for src_dst_item in src_dst_list:
        valid_ips = validate_addresses(src_dst_item, jid)
        if valid_ips == False:
            continue
        else:
            access_role_list = []
            if len(src_dst_item[1]) == 3:
                for element in src_dst_item[1]:
                    access_role_list.append(element[2] + '_' + element[1] + '_24')
            processing_item = str(src_dst_item[2])
            processing_item = processing_item.replace('\'', '')
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + "', 'Processing - From " + \
                  src_dst_item[0] + " to " + processing_item + \
                  "', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                  jid + "', 'Checking zone memberships ', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
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
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                  jid + "', 'Checking Unified Security Policy ', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
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
                sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                      "', 'Some source adresses are not a part of USP.\nPlease manually add them via Tufin Web Interface and run script again. ', '" + config.now() + \
                      "' )"
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
            if dst_zone == '':
                sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                      "', 'Some destination adresses are not a part of USP.\nPlease manually add them via Tufin Web Interface and run script again. ', '" + config.now() + \
                      "' )"
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()

            # Checking USP rules
            if src_zone != '' and dst_zone != '':
                requested_ports = src_dst_item[4].split('\n')
                if 'TCP' in requested_ports:
                    requested_ports.remove('TCP')
                matrix_intersection_pre_row = response_get_usp_df[(response_get_usp_df['from zone'] == src_zone) & (
                        response_get_usp_df['to zone'] == dst_zone)].values.tolist()
                matrix_intersection_row = matrix_intersection_pre_row[0]
                proceed = ''
                if matrix_intersection_row[3] == 'block all':
                    sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                          "', 'It violates rule \"block all\" between zones ', '" + config.now() + "' )"
                    cur = conn.cursor()
                    cur.execute(sql)
                    conn.commit()
                    break
                elif matrix_intersection_row[3] == 'block only':
                    blocked_services_list = matrix_intersection_row[4].split(';')
                    for port_i in requested_ports:
                        if port_i.lower() in blocked_services_list:
                            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                                  "', 'It violates rule \"block only\" between zones ', '" + config.now() + "' )"
                            cur = conn.cursor()
                            cur.execute(sql)
                            conn.commit()
                            break
                        else:
                            check_path(src_ip_addresses, dst_ip_addresses,
                                       src_adr_mask_list, dst_adr_mask_list, src_dst_item, jid)
                elif matrix_intersection_row[3] == 'allow only':
                    allowed_services = matrix_intersection_row[4].split(';')
                    allowed_services_list = [item.lower()
                                             for item in allowed_services]
                    for port_i in requested_ports:
                        if port_i.lower() in allowed_services_list:
                            proceed = 'Y'
                        else:
                            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + jid + \
                                  "', 'It violates rule \"allow only\" between zones ', '" + config.now() + "' )"
                            cur = conn.cursor()
                            cur.execute(sql)
                            conn.commit()
                            proceed = 'N'
                            break
                    if proceed == 'Y':
                        check_path(src_ip_addresses, dst_ip_addresses,
                                   src_adr_mask_list, dst_adr_mask_list, src_dst_item, jid, access_role_list)
                elif matrix_intersection_row[3] == 'allow all':
                    check_path(src_ip_addresses, dst_ip_addresses,
                               src_adr_mask_list, dst_adr_mask_list, src_dst_item, jid, access_role_list)
            # print(src_dst_item)
            sql = "insert into main_table('id', 'msg', 'last_updated') values('" + \
                  jid + "', 'Request Processed ', '" + config.now() + "' )"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            # input("Processing next request, please press Enter to continue or ctrl C to quit...")
