import sys
sys.path.append('../classes/')

from reddit_thread import thread

import requests
import requests.auth

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

response = requests.get("https://oauth.reddit.com/r/MakeupAddiction/comments/2x105m/what_does_mua_think_of_kim_kardashians_routine/", headers=headers)
data = response.json()

# Load thread into 'thread' object
test_thread = thread(data)

# Print ALL comments and replies
print test_thread.get_text()