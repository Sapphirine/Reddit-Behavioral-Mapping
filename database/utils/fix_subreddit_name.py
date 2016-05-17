# Initialize PRAW
import praw

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)

# Initialize DynamoDB
import boto3

dynamodb = boto3.resource('dynamodb')
t_table = dynamodb.Table('Threads')

def encode(utf8str):

    # Catch bad inputs
    if utf8str is None:
        return 'None'

    if utf8str == '':
        return 'None'

    # Catch all numericals
    if isinstance(utf8str, float) or isinstance(utf8str, long) or isinstance(utf8str, int):
        return int(utf8str)

    # Correct unicode strings
    if isinstance(utf8str, str) or isinstance(utf8str, unicode):
        utf8str = utf8str.encode('ascii','ignore')
        if utf8str.isspace():
            return 'None'
        if (utf8str == ''):
            return 'None'
        return utf8str

    # Empty lists and dicts
    if (utf8str == []) or (utf8str == {}):
        return 'None'

    else:
        return utf8str

for submission in t_table.scan()['Items']:
    if submission['subreddit'] == 'SUBREDDIT_ERR':
#        submission.update()
        t_table.update_item(
            Key={
                'id': encode(submission['id']),
                'search_term' : encode(submission['search_term'])
            },
            UpdateExpression='set subreddit = :val1',
            ExpressionAttributeValues={
                ':val1': encode(r.get_info(thing_id=submission['subreddit_id']).display_name)
            }
        )