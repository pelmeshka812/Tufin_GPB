import json
import time

import requests
from requests.auth import HTTPBasicAuth

WORKFLOW_ID = "43746ca1-b01b-4d4d-a184-d036c540797c"
body = {
    "parameters": [
        {"value": {"string": {"value": "22"}},
         "type": "string",
         "name": "Source",
         "scope": "local"
         },
        {"value": {"string": {"value": "33"}},
         "type": "string",
         "name": "Destination",
         "scope": "local"
         },
        {"value": {"string": {"value": "44"}},
         "type": "string",
         "name": "Service",
         "scope": "local"
         }
    ]
}
# r = requests.get('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/''/executions/')
# print(r.status_code, r.reason, r)
# POST_RESULT = requests.post('https://vrealize.iss.icl.kazan.ru/vco/api/workflows/' + WORKFLOW_ID + '/executions/',
#                             auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False, json=body)
POST_RESULT = requests.post('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/' + WORKFLOW_ID + '/executions/',
                            auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False, json=body)
r = requests.get(
    'https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/43746ca1-b01b-4d4d-a184-d036c540797c/executions/05aff767-974c-4a86-860f-d03db7087dd8/',
    auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False)

# r = requests.get('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/'+WORKFLOW_ID+'/executions/', auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False)
# print(POST_RESULT.status_code, POST_RESULT.content)  ## if 200/ 202 - all is zbs
print(r.status_code, r.content)
