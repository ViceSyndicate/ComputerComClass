import flask
import json
import time
from flask import request,Response, jsonify, url_for
from urllib3.util import current_time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

BASE_URL = '/v3/'

def read_posts():
    with open("posts.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def save_posts(data):
    with open("posts.json", "w") as json_file:
        json.dump(data, json_file)

def read_users():
    with open("user.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def save_users(data):
    with open("user.json", "w") as json_file:
        json.dump(data, json_file)



def read_data():
    with open("data.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_data(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


@app.route('/')
def home():
    return '<h1>O shit waddup<h1/><br/> <img src="https://cdn.shopify.com/s/files/1/0160/2840/1712/products/datboi_concept.png?v=1586043523">'


#{"id": 7,"username": "NewUser"}

@app.route(BASE_URL + 'create_user',methods = ['POST'])
def add_post():
    post_data = flask.request.json
    valid_keys = ["id", "username"]
    for key in post_data:
        if key not in valid_keys:
            return flask.Response('{"status": "Error", "reason": "Json format error. Key ' + key + 'not allowed."}',
                                  400, content_type="application/json")

        users = read_users()
        users.append(post_data)
        save_users(users)
        return flask.Response('{"status" : "Created"}', 201, content_type="application/json")


@app.route(BASE_URL + 'all', methods=['GET'])
def all_posts():
    posts = read_posts()
    json_posts = json.dumps(posts)
    return flask.Response(json_posts, 200, content_type="application/json")


@app.get('/v1/persons')
def index_get():
    # get request argument for last_name
    last_name = flask.request.args.get("last_name")
    # Read data as python list of dictionaries
    persons = read_data()
    # If request to filter on last name
    if last_name:
        # Create filtered of persons  matching the filter
        new_persons = [person for person in persons if person["last_name"] == last_name]

        persons = new_persons
    # Convert the list of dictionaries to a Json string
    json_persons = json.dumps(persons)
    return flask.Response(json_persons, 200, content_type="application/json")


@app.route('/v2/person', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    with open("data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for person in data:
        if person['id'] == id:
            results.append(person)

    return jsonify(results)


@app.get('/v2/persons')
def index_post():
    data = flask.request.json
    valid_keys = ["first_name", "last_name", "age"]
    for key in data:
        if key not in valid_keys:
            return flask.Response('{"status": "Error", "reason": "Json format error. Key ' + key + 'not allowed."}',
                                  400, content_type="application/json")
    persons = read_data()
    persons.append(data)
    save_data(persons)
    return flask.Response('{"status" : "Created"}', 201, content_type="application/json")

# Gregs/My Recent Code Starts Here


def save_posts(data):
    with open("posts.json", "w") as json_file:
        json.dump(data, json_file)


def read_all_posts():
    with open("posts.json", "r", encoding="utf-8") as posts:
        return json.load(posts)


@app.route('/login',methods = ['POST'])
def login():
    user = request.form['nm']
    user_data = flask.request.json

    return flask.redirect(url_for('success',name = user_data))


if __name__ == '__main__':
    app.run()
