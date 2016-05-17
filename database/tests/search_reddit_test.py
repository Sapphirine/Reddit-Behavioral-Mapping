import requests
import requests.auth
import json

# Information needed from account and app info
USERNAME     = 'eecse6895_1_g37_bot '
PASSWORD     = 'AccessCode1!'
CLIENTID     = 'K9zorfgU5E9_pA'
CLIENTSECRET = '-yWWa-sE0Cqz3mPUNRN6ABFlUoI'

# Request a token. For acquiring a token, requests are made to https://www.reddit.com
client_auth = requests.auth.HTTPBasicAuth(CLIENTID, CLIENTSECRET)
post_data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

# Get the token
TOKEN = response.json()['access_token']
headers = {"Authorization": "bearer {}".format(TOKEN), "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

# Search all of reddit (search for the name Kim Kardashian) and save to file
response = requests.get("https://oauth.reddit.com/search.json?q=kim+kardashian", headers=headers)
data = response.json()
with open("JSON_DUMP_KIM_SEARCH.txt","w") as outfile:
    outfile.write(json.dumps(data, indent=4, sort_keys=True))

"""
This returns posts.  The posts can then be searched.
"""

# Search single post and dump to file
response = requests.get("https://oauth.reddit.com/r/MakeupAddiction/comments/2x105m/what_does_mua_think_of_kim_kardashians_routine/", headers=headers)
data = response.json()
with open("JSON_DUMP_KIM_POST.txt","w") as outfile:
    try:
        for i in xrange(len(data)):
            outfile.write(json.dumps(data[i], indent=4, sort_keys=True))
    except:
        outfile.write(json.dumps(data, indent=4, sort_keys=True))