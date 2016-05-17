import praw
import sys
sys.path.append("../../utils/")
from utils.sql import put_thread

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)
submissions = r.search('Donald Trump', limit=10)
for submission in submissions:
    submission.replace_more_comments()
    put_thread(submission)