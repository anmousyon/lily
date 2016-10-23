'''fill the database'''
from urllib.parse import urlparse
from lily import helpers, lily
from py2neo import Node, Relationship


def add_post(graph, post, sub_node):
    post_node = Node('post', label=str(post.id))
    graph.merge(post_node)
    post_node['title'] = str(post.title)
    post_node['title_sentiment'] = helpers.sentiment(post.title)
    post_node['is_selftext'] = str(post.is_self)
    post_node['selftext'] = str(post.selftext)
    post_node['selftext_sentiment'] = helpers.sentiment(post.selftext)
    post_node['site'] = 'http://' + urlparse(str(post.url))[1].strip()
    post_node['created'] = str(post.created)
    post_node['edited'] = str(post.edited)
    post_node['karma'] = int(post.score)
    post_node['gold'] = int(post.gilded)
    post_node['link'] = str(post.permalink)
    graph.push(post_node)

    user_node = Node('user', label=str(post.author))
    graph.merge(user_node)

    graph.merge(Relationship(post_node, 'posted in', sub_node))
    graph.merge(Relationship(user_node, 'posted', post_node))

    return post_node


def add_comment(graph, comment, post_node, parent_node):
    comment_node = Node('comment', label=str(comment.id))
    graph.merge(comment_node)
    comment_node['body'] = comment.body
    comment_node['sentiment'] = helpers.sentiment(comment.body),
    comment_node['created'] = str(comment.author)
    comment_node['edited'] = str(comment.edited)
    comment_node['karma'] = int(comment.score)
    comment_node['gold'] = int(comment.gilded)
    comment_node['link'] = str(comment.permalink)
    graph.push(comment_node)

    user_node = Node('user', label=str(comment.author))
    graph.merge(user_node)

    graph.merge(Relationship(comment_node, 'commented on', parent_node))
    graph.merge(Relationship(user_node, 'commented', comment_node))

    return comment_node


def dfs(graph, comment, post_node, comment_node, seen):
    if not seen:
        seen = set()

    for reply in set(comment.replies) - seen:
        comment_node = add_comment(graph, reply, post_node, comment_node)
        seen.add(reply)
        dfs(graph, reply, post_node, comment_node, seen)


def fill(graph, reddit, sub, sub_node):
    posts = helpers.get_posts(reddit, sub)

    for post in posts:
        # print post currently working on (remove later)
        print(post.title)

        comments = helpers.comments(post)

        post_node = add_post(graph, post, sub_node)

        for top_level_comment in comments:
            comment_node = add_comment(graph, top_level_comment, post_node, post_node)
            dfs(graph, top_level_comment, post_node, comment_node, seen=None)

    print('done with sub')


def build(graph):
    '''fills the posts and comments graph'''
    reddit = helpers.login()

    subs = set()
    with open('lily/info/subreddits.txt') as file:
        subs = file.readlines()

    for sub in subs:
        sub = sub.strip()

        sub_node = Node('sub', label=sub)
        graph.merge(sub_node)

        fill(graph, reddit, sub, sub_node)

    print('done building')