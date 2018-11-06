import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apiUser = "username"
apiPassword = "password"
baseUrl = "https://FQDN or IP Here/vmrest/"
headers = {'Accept': 'application/json', 'User-Agent': 'Java/1.6.0_20', 'Host': 'FQDN Server name', 'Connection': 'keep_alive'}
username = "user123"
email = "user123@domain.com"

# locate user uuid
user = requests.get(baseUrl + "users?query=(alias is " + username + ")", auth=(apiUser, apiPassword), headers=headers, verify=False)
user_formatted = json.loads(user.text)
print(user_formatted)
num_accounts = user_formatted['@total']
int_num_accounts = int(num_accounts)
if int_num_accounts is 0:
    print('none')
else:
    objectid = user_formatted['User']['ObjectId']
    print(objectid)

# check if Unified Account exists for that UUID
s = requests.get(baseUrl + "users/" + objectid + "/externalserviceaccounts", auth=(apiUser, apiPassword), headers=headers, verify=False)
accounts_formatted = json.loads(s.text)
num_accounts = accounts_formatted['@total']
int_num_accounts = int(num_accounts)
print('number of unified accounts for user: ' + num_accounts)
print(accounts_formatted)
if int_num_accounts >= 1:
    unified_objectid = accounts_formatted['ExternalServiceAccount']['ObjectId']
    print(unified_objectid)

# if unified account exists delete it and build new O365
# will delete O365 and recreate
if int_num_accounts is not 0:
    print('Unified Account for ' + username + ' already exists')
    p = requests.delete(baseUrl + "users/" + objectid + "/externalserviceaccounts/" + unified_objectid, auth=(apiUser, apiPassword), headers=headers, verify=False)
    print(p)
    if p.status_code == 202 or p.status_code == 200 or p.status_code == 201 or p.status_code == 204:
        print('Unified Account deletion for ' + username + ' successful')
    if p.status_code == 400 or p.status_code == 404:
        print('Unified Account deletion for ' + username + ' failed')
    print('Proceeding with O365 Account Build')
    unified = {'ExternalServiceObjectId': 'e412885a-5614-4aaa-aaaa-a525e34f3a1e',  # this is the UUID of the O365 unifed messaging
               'EnableCalendarCapability': 'false',
               'EnableTtsOfEmailCapability': 'false',
               'EnableMailboxSynchCapability': 'true',
               'EmailAddressUseCorp': 'true'}
    p = requests.post(baseUrl + "users/" + objectid + "/externalserviceaccounts/", auth=(apiUser, apiPassword), headers=headers, json=unified, verify=False)
    print(p)
    if p.status_code == 202 or p.status_code == 200 or p.status_code == 201 or p.status_code == 204:
        print('Unified account build for: ' + username + ' successful')
    if p.status_code == 400 or p.status_code == 404:
        print('Unified account build for: ' + username + ' failed')
else:
    # if no unified account build O365
    print('No Unified Account for ' + username + ' exists')
    unified = {'ExternalServiceObjectId': 'e412885a-5614-4aaa-aaaa-a525e34f3a1e',  # this is the UUID of the O365 unified messaging
               'EnableCalendarCapability': 'false',
               'EnableTtsOfEmailCapability': 'false',
               'EnableMailboxSynchCapability': 'true',
               'EmailAddressUseCorp': 'true'}
    p = requests.post(baseUrl + "users/" + objectid + "/externalserviceaccounts/", auth=(apiUser, apiPassword), headers=headers, json=unified, verify=False)
    print(p)
    if p.status_code == 202 or p.status_code == 200 or p.status_code == 201 or p.status_code == 204:
        print('Unified account build for: ' + username + ' successful')
    if p.status_code == 400 or p.status_code == 404:
        print('Unified account build for: ' + username + ' failed')
