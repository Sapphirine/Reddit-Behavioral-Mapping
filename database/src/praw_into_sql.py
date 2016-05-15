import praw
from sql import put_thread, close_session

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)

# For parsing input args
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--search_term', help='String to search for')
parser.add_argument('--subreddit', help='Subreddit to constrain search to')
parser.add_argument('--sort', help='Sorting method e.g. \'hot\' or \'new\' ')
parser.add_argument('--syntax', help='?')
parser.add_argument('--period', help='?')
parser.add_argument('--limit', help='Maximum number of items to return (max=1000)', type=int)

if __name__ == '__main__':
    
    args = parser.parse_args()
    
    submissions = r.search(args.search_term, subreddit=args.subreddit, sort=args.sort, syntax=args.syntax, period=args.period, limit=args.limit)
    
    for submission in submissions:
        submission.replace_more_comments()
        put_thread(submission)
        
    close_session()
