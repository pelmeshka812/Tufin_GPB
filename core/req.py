import json
import requests

# r1 = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
# print(r.status_code, r.reason, r)
f = {"flowUuid": "Foled.Flow", "inputs": {"flow_input_0": "1", "flow_input_1": "2", "flow_input_2": "3"},
      "logLevel": "EXTENDED", "inputPromptUseBlank": "false", "triggerType": "MANUAL"}
r1 = requests.post('http://10.1.101.215:8080/oo/rest/latest/executions', json=f)
id = r1.content.decode('UTF-8')
print(r1.status_code)

body = {"action": "RESUME",
        "data": {"input_binding": {"ti1": "11", "ti2": "22", "ti3": "33"}}}
# body = json.loads(body)
r = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
print(r.status_code, r.content)


#r2 = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/' + id + '/execution-log')
#print(r2.status_code, r2.content)
dict = json.loads(r.content.decode('utf-8'))
#ВАЖНООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО
print(dict[0]["status"])
#print(dict[0]["flowoutput"])
