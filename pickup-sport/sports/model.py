# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datatime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

# [START model]
# class Book(db.Model):
#     __tablename__ = 'books'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     author = db.Column(db.String(255))
#     publishedDate = db.Column(db.String(255))
#     imageUrl = db.Column(db.String(255))
#     description = db.Column(db.String(4096))
#     createdBy = db.Column(db.String(255))
#     createdById = db.Column(db.String(255))
#
#     def __repr__(self):
#         return "<Book(title='%s', author=%s)" % (self.title, self.author)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.String(255), default="0")

    def __repr__(self):
        return "<User(name='%s', email=%s)" % (self.name, self.email)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    organizer = db.Column(db.String(255))
    players = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    length = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    description = db.Column(db.String(255))
    venueId = db.Column(db.Integer)

    def __repr__(self):
        return "<Event(name='%s', description=%s, players=%d)" % (self.organizer, self.description, self.players)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Players(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    eventId = db.Column(db.Integer)


# [END model]


def insertEvents():
    event1Dict = {"Organizer": "Austin FC", "Players": 4,"Time": datetime.datetime(2019,8,10,18),"Length": 90, "VID":1,"Capacity":20,"Description":"Pick up soccer"}
    event2Dict = {"Organizer": "Austin fan", "Players": 10,"Time": datetime.datetime(2019,8,15,19),"Length": 50, "VID":2,"Capacity":12,"Description":"Soccer Tournament"}
    event3Dict = {"Organizer": "Tennis Austin", "Players": 2,"Time": datetime.datetime(2019,8,13,18),"Length": 75, "VID":5,"Capacity":4,"Description":"Junior drop in organized by Tennis Texas club"}
    event4Dict = {"Organizer": "Austin Rockets", "Players": 3,"Time": datetime.datetime(2019,8,21,14),"Length": 65, "VID":4,"Capacity":10,"Description":"Basketball fans can not miss this"}
    event5Dict = {"Organizer": "Cricket Austin", "Players": 5,"Time": datetime.datetime(2019,8,25,10),"Length": 80, "VID":1,"Capacity":10,"Description":"League time"}
    event6Dict = {"Organizer": "Soccer@Austin", "Players": 7,"Time": datetime.datetime(2019,8,16,18,30),"Length": 70,"VID":3,"Capacity":22,"Description":"Soccer game"}
    
    event = Event(**event1Dict)
    db.session.add(event)
    db.session.commit()
    return from_sql(event)

def insertPlayers():
    player1Dict = {"userid":1, "eventid": 2}
    player2Dict = {"userid":3, "eventid": 5}

    player = Event(**player1Dict)
    db.session.add(player)
    db.session.commit()
    return from_sql(player)

def insertuser():
    userDict = { "name" : "Michael Jordan",
                 "email": "jordan@bulls.com",
                 "phone": "232323",
                  "password": "goat",
                 "admin": "1"
              }
    # venue3Dict = { "name" : "Tennis Zone North Austin",
    #             "location" : "North Austin",
    #              "description": "Outdoor Tennis stadium at North Austin",
    #           }
    # venue4Dict = { "name" : "Soccer Zone East Austin",
    #             "location" : "West Campus",
    #              "description": "Outdoor Soccer stadium at East Austin",
    #           }
    # venue5Dict = { "name" : "Basketball Field West Austin",
    #             "location" : "West Campus",
    #              "description": "Outdoor Basketball Field at West Austin",
    #           }
    # venue6Dict = { "name" : "Soccer Zone Downtown Austin",
    #             "location" : "Downtown",
    #              "description": "Indoor Tennis courts at Downtown",
    #             }

    user = User(**userDict)
    db.session.add(user)


    db.session.commit()
    return from_sql(user)


# [START list]
# def list(limit=10, cursor=None):
#     cursor = int(cursor) if cursor else 0
#     query = (Book.query
#              .order_by(Book.title)
#              .limit(limit)
#              .offset(cursor))
#     books  = builtin_list(map(from_sql, query.all()))
#     next_page = cursor + limit if len() == limit else None
#     return (books, next_page)
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (User.query
             .order_by(User.name)
             .limit(limit)
             .offset(cursor))
    users = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(users) == limit else None
    return (users, next_page)
# [END list]

def showAllEvents(limit = 10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Event.query
             .order_by(Event.organizer)
             .limit(limit)
             .offset(cursor))
    events = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(events) == limit else None
    return (events, next_page)

def showAllVenues(limit = 10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Venue.query
             .order_by(Venue.name)
             .limit(limit)
             .offset(cursor))
    venues = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(venues) == limit else None
    return (venues, next_page)

# [START read]
# def read(id):
#     result = Book.query.get(id)
#     if not result:
#         return None
#     return from_sql(result)
def read(id):
    result = User.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]

def getuser(email,password):
    # connection = db.engine.raw_connection()
    # cursor = connection.cursor()
    userInfo = User.query.filter_by(email=email).first()
    passwordInDatabase = userInfo.password
    if password == passwordInDatabase: # entered password matches one in database
        return "1"
    else:
        return "0"

# [START create]
# def create(data):
#     book = Book(**data)
#     db.session.add(book)
#     db.session.commit()
#     return from_sql(book)
def create(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return from_sql(user)
# [END create]



# [START update]
# def update(data, id):
#     book = Book.query.get(id)
#     for k, v in data.items():
#         setattr(book, k, v)
#     db.session.commit()
#     return from_sql(book)
# [END update]


# def delete(id):
#     Book.query.filter_by(id=id).delete()
#     db.session.commit()
def delete(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        # db.create_all()
        insertuser()
    # print("All tables created")
    print("User added!")

def _drop_database():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
    print("All tables dropped")

if __name__ == '__main__':
    _create_database()