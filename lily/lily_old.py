'''new main app using peewee'''
from flask import Flask, request, g, render_template
from peewee import *
from playhouse.sqlite_ext import *
import logging
from lily.build import build
from lily import helpers, classifier

#logging config
logging.basicConfig(filename='lily/info/logger.log', filemode='w', level=logging.DEBUG)

#config
DATABASE = 'lily/info/lily.db'
DEBUG = True
SECRET_KEY = 'development key'

#create the app
app = Flask(__name__)
app.config.from_object(__name__)

#create peewee database instance
SQLDB = SqliteExtDatabase(DATABASE)

class Post(Model):
    '''post model'''
    label = TextField(unique=True)
    title = TextField()
    is_self = TextField()
    selftext = TextField()
    site = TextField()
    subreddit = TextField()
    username = TextField()
    replies = IntegerField()
    created = TextField()
    edited = TextField()
    sentiment = FloatField()
    karma = IntegerField()
    gold = IntegerField()
    link = TextField()

    class Meta:
        '''define database and sort order'''
        order_by = ('karma',)
        database = SQLDB

class FTSPost(FTSModel):
    '''searchable post model'''
    label = TextField()
    title = SearchField()
    selftext = SearchField()
    site = SearchField()
    subreddit = SearchField()
    username = SearchField()

    class Meta:
        '''define database'''
        database = SQLDB
        extension_options = {'tokenize': 'porter'}

class Comment(Model):
    '''comment model'''
    label = TextField(unique=True)
    body = TextField()
    post = TextField()
    username = TextField()
    subreddit = TextField()
    replies = IntegerField()
    created = TextField()
    edited = TextField()
    sentiment = FloatField()
    karma = IntegerField()
    gold = IntegerField()
    link = TextField()

    class Meta:
        '''define order'''
        order_by = ('karma',)
        database = SQLDB

class FTSComment(FTSModel):
    '''searchable comment model'''
    label = TextField()
    body = SearchField()
    username = SearchField()
    subreddit = SearchField()

    class Meta:
        '''define database'''
        database = SQLDB
        extension_options = {'tokenize': 'porter'}

def create_tables():
    '''create tables in database'''
    SQLDB.connect()
    SQLDB.create_tables([Post, FTSPost, Comment, FTSComment], safe=True)

@app.cli.command('initdb')
def init_db():
    '''initialize the database'''
    SQLDB.init('lily/info/lily.db')
    create_tables()
    build(SQLDB)

@app.cli.command('train')
def train():
    '''train the classifier'''
    classifier.train_classifier()

@app.before_request
def before_request():
    '''connect to database'''
    g.sqlite_db = SQLDB
    g.sqlite_db.connect()

@app.after_request
def after_request(response):
    '''close connection'''
    g.sqlite_db = SQLDB
    g.sqlite_db.close()
    return response

@app.route('/')
def homepage():
    '''show top posts in database'''
    posts = Post.select().where(Post.karma > 5000).order_by(-Post.karma).limit(10)
    return render_template('show_posts.html', posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    '''search the comments by karma'''
    if request.method == 'POST':
        query = request.form['query']
        posts = helpers.search(str(query))
        return render_template('show_posts.html', posts=posts)

@app.route('/post/<post_id>')
def show_post(post_id):
    '''show the post with the given id'''
    post = Post.get(Post.label == post_id)
    print(post.label)
    return render_template('post_info.html', post=post)
