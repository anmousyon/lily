'''new main app using peewee'''
from flask import Flask, request, g, render_template
from py2neo import Graph
import logging
from lily.build import build
from lily import helpers, classifier


# create uniqueness constraints for each type of node
graph = Graph('http://neo4j:buffalo12@localhost:7474/db/data/')
for node_type in ('sub', 'user', 'post', 'comment'):
    try:
        graph.schema.create_uniqueness_constraint(node_type, 'label')
    except:
        pass

#config
DEBUG = True
SECRET_KEY = 'development key'


# create the app
app = Flask(__name__)
app.config.from_object(__name__)


@app.cli.command('build')
def init_db():
    '''build the graph'''
    build(graph)


@app.cli.command('train')
def train():
    '''train the classifier'''
    classifier.train_classifier()


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
