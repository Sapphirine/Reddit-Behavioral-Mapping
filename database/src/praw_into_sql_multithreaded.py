import praw
from sql import put_thread, close_session
from multiprocessing import Process, Queue
import time
import requests

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

# Define queue
q = Queue()

# Temporary
num_total = 0
num_finished = 0
def is_finished():
    
    if num_finished == num_total:
        return True
    return False

# Workers
def add_to_db():
    
    while True:
        submission = q.get()
        if not submission:
            if is_finished():
                return
            continue
        put_thread(submission, fast=True)
    
# Define thread to handle queues.  We will use one thread because SQLAlchemy sessions are designed to be single-threaded.
t1 = Process(target=add_to_db)
t1.start()

def recursive_search(search_term, subreddit=None, sort=None, syntax=None, period=None, limit=None):
    
    try:
        return r.search(search_term, subreddit=subreddit, sort=sort, syntax=syntax, period=period, limit=limit)
    except requests.exceptions.Timeout:
        time.sleep(30)
        return recursive_search(search_term, subreddit=subreddit, sort=sort, syntax=syntax, period=period, limit=limit)

def recursive_comments(submission):
    
    try:
        submission.replace_more_comments()
    except requests.exceptions.Timeout:
        time.sleep(30)
        recursive_comments(submission)

# Index of all submissions
submission_idx = set()
        
# Executes each search in parallel and populates queue.
def do_search(search_term, subreddit=None, sort=None, syntax=None, period=None, limit=None):
    
    global num_finished
    submissions = recursive_search(search_term, subreddit=subreddit, sort=sort, syntax=syntax, period=period, limit=limit)
    
    for submission in submissions:
        if submission.id in submission_idx:
            continue
        submission_idx.add(submission.id)
        recursive_comments(submission)
        # Add to queue
        q.put(submission)
    num_finished += 1

if __name__ == '__main__':
    
    args = parser.parse_args()
    
    # Split search terms
    search_terms = args.search_term.split(",")
    
    global num_total
    num_total = len(search_terms) 
    
    for search_term in search_terms:
        t = Process(target=do_search, args=(search_term, args.subreddit, args.sort, args.syntax, args.period, args.limit, ))
        t.daemon = True
        t.start()
    
    t1.join() # block until all tasks are done
    close_session()