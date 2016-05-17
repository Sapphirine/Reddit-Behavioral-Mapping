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
# Print response in JSON
#print response.json()
#print ''
# Get the token
TOKEN = response.json()['access_token']

# Use the token.  For using a token, requests are made to https://oauth.reddit.com
headers = {"Authorization": "bearer {}".format(TOKEN), "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
 Print response in JSON
print response.json()
print ''

# Gets comments from a reddit post (Bernie Sanders Example)
response = requests.get("https://oauth.reddit.com/r/SandersForPresident/comments/4dqy9q/important_if_youre_ever_going_to_donate_now_is/", headers=headers)
print response.json()
print ''

# Print data from comments in JSON format
data = response.json()
with open("JSON_DUMP_BERNIE.txt","w") as outfile:
    for i in xrange(len(data)):
        outfile.write(json.dumps(data[i], indent=4, sort_keys=True))

# Gets comments from a reddit post (Donald Trump Example)
response = requests.get("https://oauth.reddit.com/r/The_Donald/comments/4dsiaz/giuliani_im_voting_for_trump/", headers=headers)
print response.json()
print ''

# Print data from comments in JSON format
data = response.json()
with open("JSON_DUMP_TRUMP.txt","w") as outfile:
    for i in xrange(len(data)):
        outfile.write(json.dumps(data[i], indent=4, sort_keys=True))

## Lets see what a whole subreddit shows
response = requests.get("https://oauth.reddit.com/r/SandersForPresident/comments/", headers=headers)
print response.json()
print ''
#
data = response.json()
with open("JSON_DUMP_BERNIE_SUB.txt","w") as outfile:
    for i in xrange(len(data)):
        outfile.write(json.dumps(data['data'], indent=4, sort_keys=True))

response = requests.get("https://oauth.reddit.com/r/The_Donald/comments/", headers=headers)
print response.json()
print

data = response.json()
with open("JSON_DUMP_TRUMP_SUB.txt","w") as outfile:
    for i in xrange(len(data)):
        outfile.write(json.dumps(data['data'], indent=4, sort_keys=True))
"""
Note:

I suspect I'll use a recursive method to harvest comments and replies.
"""