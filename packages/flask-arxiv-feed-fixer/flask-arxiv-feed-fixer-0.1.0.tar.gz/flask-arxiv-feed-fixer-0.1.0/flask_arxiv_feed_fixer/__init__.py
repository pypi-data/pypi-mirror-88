__version__ = '0.1.0'

import xml.etree.ElementTree as ET

from flask import Blueprint
import requests




class ArxivFeedFixer(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        print('init arxiv')
        blueprint = Blueprint(
            'arxiv',
            __name__,
            url_prefix='/arxiv'
        )

        @blueprint.route('/<category>')
        def arxiv(category):
            r = requests.get('http://export.arxiv.org/rss/%s' % category)
            if r.ok:
                print(r.content)
                data = [line for line in r.content.split(b'\n') if b'syn:updateBase' not in line]
                print(data)
                return b'\n'.join(data)

        app.register_blueprint(blueprint)

