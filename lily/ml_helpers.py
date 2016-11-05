'''ml helpers for classifying comments'''
import time
import gc
from lily import lily, helpers


def extract(data, col):
    '''get the output for the data'''
    extracted = [row.pop(col) for row in data]
    return data, extracted


def get_data():
    '''get the data from the database'''
    comments = lily.Comment.select()
    data = [
        [
            comment.post,
            helpers.rounder(comment.replies),
            comment.subreddit,
            helpers.get_hour(comment.created),
            helpers.get_hour(comment.edited),
            str(comment.sentiment),
            helpers.rounder(comment.karma),
            helpers.simplify_bool(comment.gold)
        ]
        for comment in comments
    ]
    return data


def encode(col):
    '''encode a column'''
    unq = {}
    count = 0
    for item in col:
        if item not in unq:
            unq[item] = count
            count += 1
    enc = [val for item in col for key, val in unq.items() if item == key]
    return enc, unq


def fit_encode(data):
    '''fit all columns, encode them and recombine them'''
    encoders = []
    cols = []
    for _ in range(7):
        data, col = extract(data, col=0)
        col, encoder = encode(col)
        cols.append(col)
        encoders.append(encoder)
    data = [[col[y] for col in cols] for y, _ in enumerate(cols[0])]
    return data, encoders


def prep_data(data):
    '''clean up and format data and get classes list'''
    data, encoders = fit_encode(data)
    data, classes = extract(data, col=5)
    return data, classes, encoders
