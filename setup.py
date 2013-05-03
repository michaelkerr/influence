try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Influence Prototype',
    'author': 'Michael Kerr',
    'url': 'https://github.com/michaelkerr/influence',
    'download_url': 'https://github.com/michaelkerr/influence',
    'author_email': 'mkerr09@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'sys', 'libxml2', 'networkx', 'datetime', 'itertools','os'],
    'packages': ['influence'],
    'scripts': [],
    'name': 'Influence Prototype'
}

setup(**config)