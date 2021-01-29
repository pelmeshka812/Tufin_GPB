import json
import time

import requests
from requests.auth import HTTPBasicAuth

in_1 = '1'
in_2 = 'chmo'
in_3 = '228'
# r1 = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
# print(r.status_code, r.reason, r)
f = {"flowUuid": "Foled.Flow", "inputs": {"flow_input_0": in_1, "flow_input_1": in_2, "flow_input_2": in_3},
     "logLevel": "EXTENDED", "inputPromptUseBlank": "false", "triggerType": "MANUAL"}
#r1 = requests.post('http://10.1.101.215:8080/oo/rest/latest/executions', json=f)
# id = r1.content.decode('UTF-8')
#print(r1.status_code)
time.sleep(5)
body = {"action": "RESUME",
        "data": {"input_binding": {"ti1": "11", "ti2": "22", "ti3": "33"}}}
# body = json.loads(body)
id = '318602471'
#r = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
#print(r.status_code, type(r.content))

r2 = requests.get('https://vrealize.iss.icl.kazan.ru/vco/api/workflows?conditions=name~Increase_inputs_by1', auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False)
print(r2.status_code)
dict = json.loads(r2.content.decode('utf-8'))
# ВАЖНООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО
url = dict['link'][0]['attributes'][0]['value']

print()

#print(dict[0]["status"])
# if dict[0]["status"] == 'COMPLETED':
# dict = json.loads(r2.content.decode('utf-8'))
# print(dict[0]["flowOutput"])
