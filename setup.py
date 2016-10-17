'''setup the app'''
from setuptools import setup

setup(
    name='lily',
    packages=['lily'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest_runner',
    ],
    test_require=[
        'pytest',
    ]
)