# -*- coding: utf-8 -*-

import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from syntax import clause

def phrases(n=20, lf=' '):
    phrase_list = []
    for i in range(n):
        phrase_list.append(repr(clause()).capitalize() + '.')
    return lf.join(phrase_list)

class MainPage(webapp.RequestHandler):
    def get(self):
        n = int(self.request.get('num_phrases') or '20')
        lf = '<br>\n' if self.request.get('break_line') == 'true' else ' '

        text = phrases(n, lf)

        template_values = {
            'text': text,
            'num_phrases': self.request.get('num_phrases'),
            'checked': 'checked' if self.request.get('break_line') == 'true' else ''
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
