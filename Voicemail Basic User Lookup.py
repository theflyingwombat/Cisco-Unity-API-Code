import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apiUser = "USERNAME"
apiPassword = "password"
baseUrl = "https://FQDN or IP/vmrest/"

headers = {'Accept': 'application/json', 'User-Agent': 'Java/1.6.0_20', 'Host': 'FQDN or IP', 'Connection': 'keep_alive'}

# replaced the uuid with the UUID of the user in unity you are trying to lookup
r = requests.get(baseUrl + 'users/b0798cd4-c0bd-4363-aaa-1a71d3505288', auth=(apiUser, apiPassword), headers=headers, verify=False)
print(r.text)
print(r)

parsed = json.loads(r.text)
print(json.dumps(parsed, indent=4, sort_keys=True))
