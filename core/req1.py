import json
import time
from datetime import datetime

import requests





    #p = Rule.objects.filter(id=2)
    #print(p)
from requests.auth import HTTPBasicAuth

in_1 = '1'
in_2 = 'chmo'
in_3 = '228'
f = {"flowUuid": "Foled.Flow", "inputs": {"flow_input_0": in_1, "flow_input_1": in_2, "flow_input_2": in_3},
         "logLevel": "EXTENDED", "inputPromptUseBlank": "false", "triggerType": "MANUAL"}
r1 = requests.post('http://10.1.101.215:8080/oo/rest/latest/executions', json=f)
print('request')
print(r1.status_code)
time.sleep(5)
#r = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
r = requests.get('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/43746ca1-b01b-4d4d-a184-d036c540797c/executions/05aff767-974c-4a86-860f-d03db7087dd8/', auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False)
print(r.status_code, type(r.content))
dict = json.loads(r.content.decode('utf-8'))
print(dict)
print(datetime.now())
