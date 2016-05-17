import praw
from sql import put_thread, put_comment, session

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)
submissions = r.search('Bernie Sanders', limit=100)
for submission in submissions:
    submission.replace_more_comments()
    put_thread(submission)
#    for comment in submission.comments:
#        temp = put_comment(comment)
#        session.commit()
#        print "Successful Commit"
    #s = submission
