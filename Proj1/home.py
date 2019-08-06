import webapp2
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
from flask import Flask

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_USER_NAME = 'default_user'

def user_key(user_name=DEFAULT_USER_NAME):
    """Constructs a Datastore key for a User entity.

    We use user_name as the key.
    """
    return ndb.Key('user', user_name)


class user(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    #uid = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    aDmin = ndb.StringProperty()

class event(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    user = ndb.StructuredProperty(user)
    Eventid = ndb.IntegerProperty(indexed=False)
    Venueid = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Homepage(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('name',
                                          DEFAULT_USER_NAME)
        event_query = event.query(
            ancestor=user_key(user_name)).order(-event.date)
        events = event_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            #'events': events,
            'user_name': urllib.quote_plus(user_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Admin(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('name',
                                          DEFAULT_USER_NAME)
        event_query = event.query(
            ancestor=user_key(user_name)).order(-event.date)
        events = event_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            #'events': events,
            'user_name': urllib.quote_plus(user_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))


class AddUser(webapp2.RequestHandler):
      def get(self):
        name =self.request.get('name',DEFAULT_USER_NAME)
        email= self.request.get('email')
        u = user()

        if users.get_current_user():
            u.author = user(
                    name= users.get_current_user().name,
                    email=users.get_current_user().email())
        u.name = name
        u.email = email
        u.put()

        query_params = {'name': name}
        self.redirect('/?' + urllib.urlencode(query_params))

class AddEvent(webapp2.RequestHandler):
      def get(self):
        name =self.request.get('name',DEFAULT_USER_NAME)
        email= self.request.get('email')
        u = user()

        if users.get_current_user():
            u.author = user(
                    name= users.get_current_user().name,
                    email=users.get_current_user().email())
        u.name = name
        u.email = email
        u.put()

        query_params = {'name': name}
        self.redirect('/?' + urllib.urlencode(query_params))
        #self.redirect('/other/Event.html')
app = webapp2.WSGIApplication([
    ("/",Homepage),
    ("/admin",Admin),
    ("/signin",AddUser),
],debug=True)
