import sys
sys.path.append('../classes/')

from reddit_thread import thread

import requests
import requests.auth

# Define search term
SEARCH_TERM = "vladimir_putin"


'''
Setup
'''

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

'''
Search (for Kim Kardashian)
'''

all_posts = requests.get("https://oauth.reddit.com/search.json?q="+SEARCH_TERM, headers=headers)
all_posts = all_posts.json()
data = response.json()

'''
Go through all posts
'''
all_text = []
num_posts = 0
for post in all_posts['data']['children']:

    post_data = post['data']
    post_url = "https://oauth." + post_data['url'][12:] # Reformat url.  Theres a better way to do this

    if 'reddit' not in post_url:    # Get rid of 'imgur' posts and the like
        continue

    #try:
    response = requests.get(post_url, headers=headers)
    thread_data = thread(response.json())
    all_text += thread_data.get_text()
    num_posts += 1
    #except:
    #    continue

print all_text
print num_posts