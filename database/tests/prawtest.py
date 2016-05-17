import praw

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)

searches=r.search("Donald Trump", subreddit=None,sort='hot', syntax=None,period=None,limit=25)