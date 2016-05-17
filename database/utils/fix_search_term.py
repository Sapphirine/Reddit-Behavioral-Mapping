# Initialize PRAW
import praw

user_agent = "ChangeMeClient/0.1 by YourUsername"
r = praw.Reddit(user_agent=user_agent)

# Initialize DynamoDB
import boto3

dynamodb = boto3.resource('dynamodb')
t_table = dynamodb.Table('Threads')
c_table = dynamodb.Table('Comments')
from boto3.dynamodb.conditions import Key

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

def do_update(child, search_term):

    try:
        comment = c_table.query(KeyConditionExpression=Key('id').eq(encode(child)))['Items'][0]
    except:
        return
    if comment['search_term'] != 'None':
        return
    if comment['children'] != 'None':
        for c in comment['children'].split(','):
            do_update(c, search_term)
    t_table.update_item(
        Key={
            'id': encode(comment['id']),
            'search_term' : 'None'
        },
        UpdateExpression='set search_term = :val1',
        ExpressionAttributeValues={
            ':val1': search_term
        }
    )

for submission in t_table.scan()['Items']:
    search_term = encode(submission['search_term'])
    for child in submission['children'].split(','):
        do_update(child, search_term)
