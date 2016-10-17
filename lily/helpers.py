'''helper functions for added analytics'''

from datetime import datetime
import logging
from math import log10, floor
from textblob import TextBlob
import praw
import RAKE
from lily import lily


FILTER = RAKE.Rake('lily/info/stoplist.txt')


def get_posts(reddit, sub):
    '''get all posts not in the database already'''
    #ids = [post.label for post in lily.Post.select().where(lily.Post.subreddit == sub)]
    ids = []
    posts = [post for post in reddit.get_subreddit(sub).get_hot(limit=10) if post.id not in ids]
    logging.info(sub)
    logging.info(len(posts))
    return posts


def get_comments(post):
    '''return an array of the comments from the post'''
    post.replace_more_comments(limit=1, threshold=10)
    return post.comments


def sentiment(text):
    '''return the sentiment that textblob calculates and simplify it to -1, 0 or 1'''
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > .2:
        return 1
    elif -0.2 <= sentiment <= 0.2:
        return 0
    else:
        return -1


def simplify_bool(boolean):
    '''change boolean string to 1 or 0'''
    return '1' if boolean == 'True' else '0'


def get_hour(time):
    '''get hour from datetime'''
    return str((datetime.fromtimestamp(int(float(time)))).hour) if time == 'True' else 0


def rounder(val):
    '''round the number down to most significant digit'''
    return str(int(round(val, -int(floor(log10(abs(int(val)))))))) if val else '0'


def get_terms(text):
    '''get most popular keyword'''
    text = FILTER.run(text)
    return text[0][0] if text else ' '


def search(term):
    '''search the database based on predicted class of search term'''
    post_items = (
        lily.Post
        .select()
        .join(
            lily.FTSPost,
            on=(lily.Post.label == lily.FTSPost.label)
        )
        .where(lily.FTSPost.match(term))
        .order_by(lily.FTSPost.bm25())
    )
    return post_items


def redditlogin():
    '''login to reddit using praw'''
    keys = []
    with open('lily/info/keys.txt') as file:
        keys = file.readlines()
    reddit = praw.Reddit('lily')
    reddit.login(keys[0].strip(), keys[1].strip(), disable_warning=True)
    return reddit
