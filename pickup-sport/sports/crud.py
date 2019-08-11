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

from sports import get_model
from flask import Blueprint, redirect, render_template, request, url_for

import ast

crud = Blueprint('crud', __name__)


# [START list]
@crud.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form.to_dict(flat=True)
        userCreated = get_model().create(user)
        if (userCreated):
            print("yes")
            return redirect("/")
        else:
            print("no")

    return render_template("signup.html")

@crud.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        email = data['email']
        password = data['password']
        print("email: {}".format(email))
        userId = get_model().getuser(email,password)
        if userId == "0":
            print("wrong credentials")
            return render_template("home.html", credentials = userId)
        else:
            return redirect("/events/{}".format(userId))

    return render_template("home.html", user={})

@crud.route('/events/<id>')
def showEventsById(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events = get_model().showEventsByUser(id)

    users = get_model().getUserById(id)
    return render_template("myevents.html", events = events, users = users)

@crud.route('/<id>')
def view(id):
    user = get_model().read(id)
    return render_template("view.html", user=user)

@crud.route('/<id>/events', methods=['GET', 'POST'])
def showEvents(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().showAllEvents(cursor=token)
    users = get_model().getUserById(id)
    venues, next_page_token = get_model().showAllVenues(cursor=token)

    if request.method == 'POST':
        venueSelected = request.form.get("venues")
        print(type(venueSelected))
        print("venue selected: {}".format(venueSelected))
        print("venue selected: {}".format(venueSelected.find('id')))
        idIndex = venueSelected.find('id') + 5
        venueId = venueSelected[idIndex]
        print("venue selected: {}".format(venueId))
        filteredEvents = get_model().showEventByVenue(venueId)
        print("events by venue: {}".format(events))

        return render_template("events.html", events=filteredEvents, users = users, venues = venues)


    return render_template("events.html", events = events, next_page_token = next_page_token, users = users, venues = venues)

@crud.route('/<uid>/join/<eid>', methods=['GET', 'POST'])
def joinEvent(uid, eid):

    events = get_model().getEventById(eid)
    users = get_model().getUserById(uid)

    if request.method == 'POST':
        userAdded = get_model().addUserToEvent(uid, eid)
        if not userAdded:
            print("User cannot be added to this event")
        else:
            return redirect("/events/{}".format(uid))

    return render_template("join.html", events = events)

@crud.route('/events')
def showAllEvents():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().showAllEvents(cursor=token)
    venues, next_page_token = get_model().showAllVenues(cursor=token)

    return render_template("browseEvents.html", events = events, venues = venues, next_page_token = next_page_token)

@crud.route('/venues')
def showAllVenues():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    venues, next_page_token = get_model().showAllVenues(cursor=token)
    return render_template("venues.html", venues = venues, next_page_token = next_page_token)

# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = get_model().create(data)

        return redirect(url_for('.view', id=user['id']))

    return render_template("form.html", action="Add", user={})


### Admin: ####

@crud.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        email = data['email']
        password = data['password']
        print("email: {}".format(email))
        userId = get_model().getadmin(email, password)
        if userId == "0":
            print("wrong credentials")
            return render_template("admin.html")
        else:
            return redirect("/admin/events/{}".format(userId))

    return render_template("admin.html", user={})

@crud.route('/admin/events/<id>')
def showEventsByIdAdmin(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events = get_model().showEventsByUser(id)

    users = get_model().getUserById(id)
    return render_template("adminevents.html", events = events, users = users)

@crud.route('/admin/events', methods=['GET', 'POST'])
def showAllEventsAdmin():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().showAllEvents(cursor=token)
    venues, next_page_token = get_model().showAllVenues(cursor=token)

    if request.method == 'POST':
        eventSelected = request.form.get("events")
        print(type(eventSelected))
        eventDict = ast.literal_eval(eventSelected)
        eventId = eventDict['id']
        print("event id: {}".format(eventId))
        get_model().deleteEvent(eventId)
        return redirect("/admin/events")

    return render_template("browseEventsAdmin.html", events = events, venues = venues, next_page_token = next_page_token)

@crud.route('/admin/users', methods=['GET', 'POST'])
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    users, next_page_token = get_model().list(cursor=token)

    if request.method == 'POST':
        userSelected = request.form.get("users")
        print(type(userSelected))
        userDict = ast.literal_eval(userSelected)
        userId = userDict['id']
        print("user id: {}".format(userId))
        get_model().deleteUser(userId)

        return redirect("/admin/users")

    return render_template(
        "adminUsers.html",
        users=users,
        next_page_token=next_page_token)

@crud.route('/admin/venues', methods=['GET', 'POST'])
def showAllVenuesAdmin():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    venues, next_page_token = get_model().showAllVenues(cursor=token)

    if request.method == 'POST':
        venueSelected = request.form.get("venues")
        print(type(venueSelected))
        venueDict = ast.literal_eval(venueSelected)
        venueId = venueDict['id']
        print("venue id: {}".format(venueId))
        get_model().deleteVenue(venueId)
        return redirect("/admin/venues")

    return render_template("adminVenues.html", venues = venues, next_page_token = next_page_token)

@crud.route('/admin/add', methods=['GET','POST'])
def addVenue():
    if request.method == 'POST':
        venue = request.form.to_dict(flat=True)
        venueCreated = get_model().createVenue(venue)
        if (venueCreated):
            print("yes")
            return redirect("/admin/venues")
        else:
            print("no")

    return render_template("adminAddVenue.html")

@crud.route('/<id>/delete')
# def delete(id):
#     get_model().delete(id)
#     return redirect(url_for('.list'))
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))