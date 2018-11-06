import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apiUser = "username"
apiPassword = "password"
baseUrl = "https://FQDN or IP/vmrest/"

ldap_id = 'user123'
dn = '12345'
# locate user information from unity user import
headers = {'Accept': 'application/json', 'User-Agent': 'Java/1.6.0_20', 'Host': 'FQDN or IP of server', 'Connection': 'keep_alive'}
r = requests.get(baseUrl + 'users?query=(DtmfAccessId is ' + dn + ')', auth=(apiUser, apiPassword), headers=headers, verify=False)
print(r)
parsed = json.loads(r.text)
print(parsed)
# find pkid which is needed for user import
value = parsed['@total']
print(value)

# prints out information in a nice view
print(json.dumps(parsed, indent=4, sort_keys=True))

# find user's ldap pkid based on user id
r = requests.get(baseUrl + 'import/users/ldap?query=(alias is ' + ldap_id + ')', auth=(apiUser, apiPassword), headers=headers, verify=False)
print(r)
parsed = json.loads(r.text)['ImportUser']
# find pkid which is needed for user import
value = parsed['pkid']
print(value)

# prints out information in a nice view
print(json.dumps(parsed, indent=4, sort_keys=True))
