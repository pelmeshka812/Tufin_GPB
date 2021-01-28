import json
import time

import requests
from requests.auth import HTTPBasicAuth

WORKFLOW_ID = "5e8f698f-a130-4f8f-86a5-37d35e6611e4"
body = {
    "parameters": [
        {"value": {"string": {"value": "22"}},
         "type": "string",
         "name": "ti1",
         "scope": "local"
         },
        {"value": {"string": {"value": "33"}},
         "type": "string",
         "name": "ti2",
         "scope": "local"
         },
        {"value": {"string": {"value": "44"}},
         "type": "string",
         "name": "ti1",
         "scope": "local"
         }
    ]
}
# r = requests.get('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/''/executions/')
# print(r.status_code, r.reason, r)
# POST_RESULT = requests.post('https://vrealize.iss.icl.kazan.ru/vco/api/workflows/' + WORKFLOW_ID + '/executions/',
#                             auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False, json=body)
POST_RESULT = requests.post('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/164a5bec-6b58-4d6e-889f-50117df2d537/executions/',
                            auth=HTTPBasicAuth('vro_api_user@vcenter.local', '1Q2w3e4r@'), verify=False, json=body)


print(POST_RESULT.status_code, POST_RESULT.content)  ## if 200/ 202 - all is zbs
