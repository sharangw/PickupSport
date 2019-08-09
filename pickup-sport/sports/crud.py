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

import cgi

crud = Blueprint('crud', __name__)


# [START list]
@crud.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        email = data['email']
        password = data['password']
        print("here: {}, {}".format(email, password))
        userId = get_model().getuser(email,password)
        if userId == "0":
            print("no no no")
        else:
            return redirect("/{}/events".format(userId))


    return render_template("home.html", user={})

@crud.route('/<id>/events')
def showEvents(id):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events = get_model().showEventsByUser(id)
    # events, next_page_token = get_model().showAllEvents(cursor=token)
    # return redirect("/{}/events.html".format(id))
    return render_template("events.html", events = events)

@crud.route('/<id>')
def view(id):
    user = get_model().read(id)
    return render_template("view.html", user=user)
# def view(id):
#     book = get_model().read(id)
#     return render_template("view.html", book=book)

@crud.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        email = data['email']
        password = data['password']
        print("here: {}, {}".format(email, password))
        isUser = get_model().getuser(email,password)
        if isUser == "1":
            return redirect("events.html")
        else:
            print("no no no")

    return render_template("admin.html", user={})

@crud.route('/admin/users')
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    users, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        users=users,
        next_page_token=next_page_token)
# [END list]
# def list():
#     token = request.args.get('page_token', None)
#     if token:
#         token = token.encode('utf-8')
#
#     books, next_page_token = get_model().list(cursor=token)
#
#     return render_template(
#         "list.html",
#         =,
#         next_page_token=next_page_token)

@crud.route('/venues')
def showVenues():
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
# def add():
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=True)
#
#         book = get_model().create(data)
#
#         return redirect(url_for('.view', id=book['id']))
#
#     return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
# def edit(id):
#     book = get_model().read(id)
#
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=True)
#
#         book = get_model().update(data, id)
#
#         return redirect(url_for('.view', id=book['id']))
#
#     return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
# def delete(id):
#     get_model().delete(id)
#     return redirect(url_for('.list'))
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))