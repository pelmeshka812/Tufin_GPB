import pdb
import subprocess
import json
import requests
import ipaddress
import io
import pandas as pd
# import checkpoint_add_new_rule
import sqlite3
import time
import urllib3
import datetime
# import _access_role_methods
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# src_dst_list = [['Администраторы Linux', [['ex1105', '172.16.200.15', 'none'], ['ex0105', '172.16.200.230', 'none'], ['ex0105', '172.16.200.128', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '443'], ['TCP', 443]], 'TCP\nHTTPS', 'Тестовый комментарий третий'], ['Прикладные администраторы', [['gpbu0105', '10.3.3.211', 'none'], ['gpbu0106', '10.3.3.119', 'none'], ['gpbu0107', '10.3.3.14', 'none']], [['192.168.100.2', 'none'], ['192.168.100.5', 'none'], ['192.168.100.101', 'none'], ['192.168.100.240', 'none'], ['192.168.100.202', 'none']], [['TCP', '445'], ['TCP', 443], ['TCP', 22]], 'TCP\nHTTPS\nSSH', 'Тестовый комментарий первый']]
exec(open("/etc/ansible/awx_playbooks/ansible_secops_test/ansible_python/usp_cleared.py").read())
src_ip_addresses = src_ip_addresses()
dst_ip_addresses = dst_ip_addresses()
src_dst_passed = src_dst_passed()
access_role_list = access_role_list()

def check_path():
    for src_dst_item in src_dst_passed:
        pdb.set_trace()
        tufin_api_user = 'admin'
        tufin_api_password = '1q2w3e'
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
        pdb.set_trace()
        for source in src_ip_addresses:
            for destination in dst_ip_addresses:  
                print('Starting Process')      
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
                    print('Path Found')
                    for dvc_info in response['path_calc_results']['device_info']:
                        device_name = dvc_info['name'].strip("'")
                        if dvc_info['vendor'] == "Generic":
                            tufin_all_url = 'https://10.1.101.210/securetrack/api/devices/'
                            headers_id = {'Content-type': 'application/json',
                                        'Accept': 'application/json'}
                            resp_devices = requests.get(tufin_all_url, headers=headers_id, auth=(
                                tufin_api_user, tufin_api_password), verify=False)
                            response_devices = json.loads(resp_devices.content)
                            for device_resp in response_devices['devices']['device']:
                                if device_resp['name'] == dvc_info['name']:                                
                                    print('Adding new rule to NSX')                                                     
                            cmd_src_dst_item = src_dst_item
                            for items in cmd_src_dst_item[1]:
                                if len(items) > 2:
                                    items.remove(items[2])
                            cmd_src_dst_item.remove(cmd_src_dst_item[4])
                            nsx_cmd = str(cmd_src_dst_item)
                            nsx_cmd = 'pwsh testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' + nsx_cmd + '"' # For Linix
                            # nsx_cmd = 'powershell.exe testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' # For Windows
                            #pscommand = 'testRestGPB.ps1 -NsxManagerIp 10.1.101.72 -Action Create -JsonQueryAsString "' # For Windows
                            #nsx_resp = subprocess.Popen(['powershell.exe', '-NoProfile', '-Command', '"&{' + pscommand + '}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            # nsx_resp = subprocess.run(nsx_cmd, shell=True, stdout=subprocess.PIPE)
                            print('Rule Added')
                            
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
                                        chkpnt_addrole_resp = _access_role_methods.add_access_role(mgmt_ip,tufin_api_user, tufin_api_password, access_role, **params)
                                        print(chkpnt_addrole_resp)
                                    print('Adding new rule for checkpoint ASTU') 
                                    chkpnt_addrule_resp = checkpoint_add_new_rule.add_new_rule(mgmt_ip, dvc_info['name'], access_role_list, None, dst_ip_addresses, services_list, None)
                                    if chkpnt_addrule_resp == True:
                                        print('Rule Added')
                                    else:
                                        print('Failed to add rule')
                                else:
                                    checkpoint_resp = checkpoint_add_new_rule.add_new_rule(
                                        mgmt_ip, dvc_info['name'], None, src_ip_addresses, dst_ip_addresses, services_list, None)
                                    print(checkpoint_resp)
                                    if chkpnt_addrule_resp == True:
                                        print('Rule Added')
                                    else:
                                        print('Failed to add rule')
                            else:
                                print('Addig new rule to checkpoint')
                                checkpoint_resp = checkpoint_add_new_rule.add_new_rule(mgmt_ip, dvc_info['name'], None, src_ip_addresses, dst_ip_addresses, services_list, None)
                                if checkpoint_resp == True:
                                    print('Checkpoint rule added')
                                else:
                                    print('Checkpoint rule failed')
                                print(checkpoint_resp)                            
                    break
                else:
                    print('Path not found')
                break
            break

result = check_path()