'''tests for helpers module'''
from lily import helpers

def test_simplify_bool():
    '''test simplify_bool'''
    assert helpers.simplify_bool("True") == "1"
    assert helpers.simplify_bool("False") == "0"
    assert helpers.simplify_bool("fdsf") == "0"

def test_simplify_sentiment():
    '''test seimplify_sentiment'''
    assert helpers.simplify_sentiment(".5") == 1
    assert helpers.simplify_sentiment(".2") == 0
    assert helpers.simplify_sentiment(".1") == 0
    assert helpers.simplify_sentiment("0") == 0
    assert helpers.simplify_sentiment("-.1") == 0
    assert helpers.simplify_sentiment("-.2") == 0
    assert helpers.simplify_sentiment("-0.5") == -1
    assert helpers.simplify_sentiment(None) == 0

def test_get_hour():
    '''test get_hour'''

def test_rounder():
    '''test rounder'''
    assert helpers.rounder(5321) == "5000"
    assert helpers.rounder(400) == "400"
    assert helpers.rounder(0) == "0"
    assert helpers.rounder(-300) == "-300"
    assert helpers.rounder(-4324) == "-4000"

def main():
    '''test everything'''
    test_simplify_bool()
    test_simplify_bool()
    test_get_hour()
    test_rounder()

main()
