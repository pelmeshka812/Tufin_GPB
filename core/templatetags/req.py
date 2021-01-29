from datetime import datetime

from django import template
import requests
import time

register = template.Library()


@register.simple_tag
def req(src,dst, port):
    src = src
    dst = dst
    port = port
    f = {"flowUuid": "Foled.Flow", "inputs": {"flow_input_0": src, "flow_input_1": dst, "flow_input_2": port},
         "logLevel": "EXTENDED", "inputPromptUseBlank": "false", "triggerType": "MANUAL"}
    r1 = requests.post('http://10.1.101.215:8080/oo/rest/latest/executions', json=f)
    print('request')
    print(r1.status_code)
    time.sleep(5)
    r = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
    print(r.status_code, type(r.content))
    print(datetime.now(), 'badddd')
    f = open("test.txt", "w", encoding="UTF8")
    f.write(str(datetime.now()))