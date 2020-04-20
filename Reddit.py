import praw
import datetime
import os
import boto3


class Reddit:
    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'], password=os.environ['REDDIT_PASSWORD'],
                         user_agent=os.environ['USER_AGENT'], username=os.environ['REDDIT_USERNAME'])
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                              endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")
    data = dynamodb.Table('dankExchangePosts')

    def scan(self):
        retour = []
        for submission in self.reddit.subreddit('dankexchange').new(limit=1000):
            time_delta = int((int(datetime.datetime.timestamp(datetime.datetime.today())) - submission.created_utc) / 60)
            posted_at = datetime.datetime.fromtimestamp(submission.created_utc).strftime('%H:%M:%S')
            if time_delta > 1440:
                break
            response = self.data.update_item(
                Key={'id': submission.id},
                UpdateExpression='SET #attr1 = :val1',
                ExpressionAttributeNames={'#attr1': f"{time_delta:03d}"},
                ExpressionAttributeValues={':val1': str(submission.score)}
            )
        return retour
