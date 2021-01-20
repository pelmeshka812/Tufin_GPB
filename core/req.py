import requests
r = requests.post('http://10.1.101.215', data={'number':2525})
print(r.status_code, r.reason)
