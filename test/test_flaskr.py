# -*- coding: utf-8 -*-
"""
    lily Tests
    ~~~~~~~~~~~~

    Tests the lily application.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import pytest

import os
import lily
import tempfile


@pytest.fixture
def client(request):
    db_fd, lily.app.config['DATABASE'] = tempfile.mkstemp()
    lily.app.config['TESTING'] = True
    client = lily.app.test_client()
    with lily.app.app_context():
        lily.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(lily.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, lily.app.config['USERNAME'],
               lily.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, lily.app.config['USERNAME'] + 'x',
               lily.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, lily.app.config['USERNAME'],
               lily.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(client):
    """Test that messages work"""
    login(client, lily.app.config['USERNAME'],
          lily.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
