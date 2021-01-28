import requests

# r1 = requests.get('http://10.1.101.215:8080/oo/rest/latest/executions/')
# print(r.status_code, r.reason, r)
r1 = requests.get('https://vrealize.iss.icl.kazan.ru:443/vco/api/workflows/5e8f698f-a130-4f8f-86a5-37d35e6611e4/')
id = r1.content.decode('UTF-8')
print(r1.status_code)