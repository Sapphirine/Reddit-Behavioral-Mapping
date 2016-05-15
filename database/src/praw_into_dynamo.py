import sys
sys.path.append("../../lib/")

# Initialize PRAW
import praw

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)

# Initialize DynamoDB
import boto3

dynamodb = boto3.resource('dynamodb')
t_table = dynamodb.Table('Threads')
c_table = dynamodb.Table('Comments')

# For logging erros and saving unentered comments
try:
   import cPickle as pickle
except:
   import pickle
import time
import logging

# For parsing input args
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--search_term', help='String to search for')
parser.add_argument('--subreddit', help='Subreddit to constrain search to')
parser.add_argument('--sort', help='Sorting method e.g. \'hot\' or \'new\' ')
parser.add_argument('--syntax', help='?')
parser.add_argument('--period', help='?')
parser.add_argument('--limit', help='Maximum number of items to return (max=1000)', type=int)

# Ensure keys are valid
def encode(utf8str):

    # Catch bad inputs
    if utf8str is None:
        return 'None'

    # Catch boolean
    if isinstance(utf8str, bool):
        return utf8str

    # Catch all numericals
    if isinstance(utf8str, float) or isinstance(utf8str, long) or isinstance(utf8str, int):
        return int(utf8str)

    if isinstance(utf8str, list) or isinstance(utf8str, dict):
        utf8str = str(utf8str)

    utf8str = utf8str.encode('ascii','ignore')
    if utf8str.isspace():
        return 'None'
    if utf8str == '':
        return 'None'
    return utf8str
    '''
    # Correct unicode strings
    if isinstance(utf8str, str) or isinstance(utf8str, unicode):
        utf8str = utf8str.encode('ascii','ignore')
        if utf8str.isspace():
            return 'None'
        if utf8str == '':
            return 'None'
        return utf8str

    # Empty lists and dicts
    if isinstance(utf8str, list):
        if utf8str == []:
            return 'None'
        utf8str = utf8str.encode('ascii','ignore')
        if utf8str == '':
            return 'None'
        if utf8str.isspace():
            return 'None'
        retur utf8str

    if isinstance(utf8str, dict):
        if utf8str == {}:
            return 'None'
        utf8str = utf8str.encode('ascii','ignore')
        if utf8str == '':
            return 'None'
        if utf8str.isspace():
            return 'None'
        retur utf8str

    # Catch and log new types
    else:
        #logging.info('TYPE {}'.format(type(utf8str)))
        #logging.info('CONTENTS: {}'.format(str(utf8str)))
        return utf8str

    '''
def get_comments(comments, search_term):

    try:

        with c_table.batch_writer() as batch:
            for comment in comments:
                # Error handling
                author = encode(comment.author.name) if isinstance(comment.author, praw.objects.Redditor) else encode(comment.author)

                batch.put_item(
                    Item={
                        'approved_by':             encode(comment.approved_by),
                        'archived':                encode(comment.archived),
                        'author':                  author,
                        'author_flair_css_class':  encode(comment.author_flair_css_class),
                        'author_flair_text':       encode(comment.author_flair_text),
                        'banned_by':               encode(comment.banned_by),
                        'body':                    encode(comment.body),
                        'body_html':               encode(comment.body_html),
                        'controversiality':        encode(comment.controversiality),
                        'created':                 encode(comment.created),
                        'created_utc':             encode(comment.created_utc),
                        'distinguished':           encode(comment.distinguished),
                        'downs':                   encode(comment.downs),
                        'edited':                  encode(comment.edited),
                        'gilded':                  encode(comment.gilded),
                        'id':                      encode(comment.id),
                        'likes':                   encode(comment.likes),
                        'link_id':                 encode(comment.link_id),
                        'mod_reports':             encode(comment.mod_reports),
                        'name':                    encode(comment.name),
                        'num_reports':             encode(comment.num_reports),
                        'parent_id':               encode(comment.parent_id),
                        'removal_reason':          encode(comment.removal_reason),
                        'children':                encode(','.join([r.id for r in comment.replies])),
                        'search_term':             encode(search_term),
                        'ups':                     encode(comment.ups),
                        'user_reports':            encode(comment.user_reports)
                    }
                )
    # To catch errors in encoding
    except Exception as e:

        logging.debug(str(e))
        t = str(time.time()).split('.')[0]
        logging.debug('PICKLING BAD COMMENTS: {}'.format(t))
        with open('../logs/comments_{}.dump'.format(t), 'wb') as dumpfile:
            pickle.dump(comments, dumpfile)
        with open('../logs/comments_{}.log'.format(t), 'w') as logfile:
            logfile.write('ERR=' + str(e) + '\n')
            logfile.write('SEARCH_TERM=' + search_term + '\n')

def search_reddit(search_term, subreddit=None, sort=None, syntax=None, limit=None, period=None):

    # Iterate through Threads
    num_submissions = 1
    for submission in r.search(search_term, subreddit=subreddit, sort=sort, syntax=syntax, period=period, limit=limit):

        logging.info('Number of Submissions: %d' % num_submissions)
        num_submissions += 1

        # get all comments and replies
        submission.replace_more_comments()
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        get_comments(flat_comments, search_term)

        author = encode(submission.author.name) if isinstance(submission.author, praw.objects.Redditor) else encode(submission.author)
        subreddit = encode(submission.subreddit.display_name) if isinstance(submission.subreddit, praw.objects.Subreddit) else encode(submission.subreddit)

        t_table.put_item(
            Item={
                'approved_by':           encode(submission.approved_by),
                'archived':              encode(submission.archived),
                'author':                author,
                'author_flair_css_class':encode(submission.author_flair_css_class),
                'banned_by':             encode(submission.banned_by),
                'clicked':               encode(submission.clicked),
                'created':               encode(submission.created),
                'created_utc':           encode(submission.created_utc),
                'distinguished':         encode(submission.distinguished),
                'domain':                encode(submission.domain),
                'downs':                 encode(submission.downs),
                'edited':                encode(submission.edited),
                'from_id':               encode(submission.from_id),
                'from_kind':             encode(submission.from_kind),
                'gilded':                encode(submission.gilded),
                'hidden':                encode(submission.hidden),
                'hide_score':            encode(submission.hide_score),
                'id':                    encode(submission.id),
                'is_self':               encode(submission.is_self),
                'likes':                 encode(submission.likes),
                'link_flair_css_class':  encode(submission.link_flair_css_class),
                'link_flair_text':       encode(submission.link_flair_text),
                'locked':                encode(submission.locked),
                'media':                 encode(submission.media),
                'media_embed':           encode(submission.media_embed),
                'mod_reports':           encode(submission.mod_reports),
                'name':                  encode(submission.name),
                'num_comments':          encode(submission.num_comments),
                'num_reports':           encode(submission.num_reports),
                'over_18':               encode(submission.over_18),
                'permalink':             encode(submission.permalink),
                'quarantine':            encode(submission.quarantine),
                'removal_reason':        encode(submission.removal_reason),
                'report_reasons':        encode(submission.report_reasons),
                'saved':                 encode(submission.saved),
                'score':                 encode(submission.score),
                'secure_media':          encode(submission.secure_media),
                'secure_media_embed':    encode(submission.secure_media_embed),
                'selftext':              encode(submission.selftext),
                'selftext_html':         encode(submission.selftext_html),
                'stickied':              encode(submission.stickied),
                'subreddit':             subreddit,
                'subreddit_id':          encode(submission.subreddit_id),
                'suggested_sort':        encode(submission.suggested_sort),
                'thumbnail':             encode(submission.thumbnail),
                'title':                 encode(submission.title),
                'ups':                   encode(submission.ups),
                'url':                   encode(submission.url),
                'user_reports':          encode(submission.user_reports),
                'visited':               encode(submission.visited),
                'search_term':           encode(search_term),
                'children':              encode(','.join([comment.id for comment in submission.comments]))
             }
         )

if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(filename='../logs/{0}_{1}.log'.format(''.join(args.search_term.split()), str(time.time()).split('.')[0]), level=logging.DEBUG)
    search_reddit(search_term=args.search_term,
                  subreddit=args.subreddit,
                  sort=args.sort,
                  syntax=args.syntax,
                  period=args.period,
                  limit=args.limit)
