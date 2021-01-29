import json
from datetime import datetime

from django import template
import requests
import time

register = template.Library()


@register.simple_tag
def req(rule):
    if rule.status != "COMPLETE":
        src = rule.source
        dst = rule.destination
        port = rule.port
        f = {"flowUuid": "Foled.Flow", "inputs": {"flow_input_0": src, "flow_input_1": dst, "flow_input_2": port},
             "logLevel": "EXTENDED", "inputPromptUseBlank": "false", "triggerType": "MANUAL"}
        r1 = requests.post('http://10.1.101.215:8080/oo/rest/latest/executions', json=f)
        print('request')
        print(r1.status_code)
        time.sleep(5)
        r = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
        print(r.status_code, type(r.content))
        dict = json.loads(r.content.decode('utf-8'))
        st = dict[0]["status"]
        rule.status = st
        rule.save()
        print(st)
        print(datetime.now(), 'badddd')
        f = open("test.txt", "w", encoding="UTF8")
        f.write(str(datetime.now()))
        return r.status_code