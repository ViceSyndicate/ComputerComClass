import flask
import json
import uuid
import time
from flask import request,Response, jsonify, url_for
from urllib3.util import current_time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

BASE_URL = '/v3/'


class User:
    uuid = uuid.uuid4()

    def __init__(self, name):
        self.id = id
        self.name = name


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


@app.route(BASE_URL + 'create_user',methods = ['POST'])
def add_user():
    post_data = request.args
    valid_keys = ["username"]
    for key in post_data:
        if key not in valid_keys:
            return flask.Response('{"status": "Error", "reason": "Json format error. Key ' + key + 'not allowed."}',
                                  400, content_type="application/json")

        new_username = post_data.get("username")
        new_uuid = uuid.uuid4()
        new_id = str(new_uuid)

        user_dictionary = read_users()

        for users in user_dictionary:
            if users.get("username") == new_username:
                return flask.Response('{"status" : "Username Already Exists."}', 418, content_type="application/json")

        new_user = {'id': new_id, 'username': new_username}
        user_dictionary.append(new_user)
        save_users(user_dictionary)
        return flask.Response('{"status" : "Created"}', 201, content_type="application/json")


@app.route(BASE_URL + 'create_post', methods = ['POST'])
def add_post():
    post_data = request.args
    valid_keys = ["username", 'content']
    for key in post_data:
        if key not in valid_keys:
            return flask.Response('{"status": "Error", "reason": "Json format error. Key ' + key + 'not allowed."}',
                                  400, content_type="application/json")

        post_id = str(uuid.uuid4())
        username = post_data.get("username")
        content = post_data.get("content")
        #post_data.update({"id": post_id})

        new_post = {'id': post_id, 'username': username, 'content': content}

        posts = read_posts()
        posts.append(new_post)
        save_posts(posts)
        return flask.Response('{"status" : "Created"}', 201, content_type="application/json")


@app.route(BASE_URL + 'get_all_posts', methods=['GET'])
def all_posts():
    posts = read_posts()
    json_posts = json.dumps(posts)
    return flask.Response(json_posts, 200, content_type="application/json")


@app.route(BASE_URL + 'get_all_users', methods=['GET'])
def all_users():
    users = read_users()
    json_posts = json.dumps(users)
    return flask.Response(json_posts, 200, content_type="application/json")


@app.route(BASE_URL + 'get_user', methods=['GET'])
def get_user():
    if 'username' in request.args:
        username = str(request.args['username'])
    else:
        return "Error: No id field provided. Please specify a username."

    results = []
    with open("user.json", "r", encoding="utf-8") as json_file:
        users = json.load(json_file)

    for user in users:
        if user['username'] == username:
            results.append(user)

    return jsonify(results)


@app.route(BASE_URL + 'get_posts_by_user', methods=['GET'])
def get_posts_by_user():
    if 'username' not in request.args:
        return "Error: No username field provided."

    username = str(request.args['username'])

    with open("user.json", "r", encoding="utf-8") as json_file:
        users = json.load(json_file)

    with open("posts.json", "r", encoding="utf-8") as json_file:
        posts = json.load(json_file)

    results = []
    for post in posts:
        if post.get('username') == username:
            results.append(post)

    return jsonify(results)


# WIP
@app.route(BASE_URL + 'delete_post', methods=['POST'])
def delete_post_by_id():
    if 'id' not in request.args:
        return "Error: No id field provided."
    code_id = str(request.args['id'])

    all_posts = read_all_posts()
    pos_to_delete = None
    for i in range(len(all_posts)):
        if str(all_posts[i].get('id')) == code_id:
            pos_to_delete = i

    if pos_to_delete is None:
        return "Error: Could not find post with this id."

    del all_posts[pos_to_delete]

    save_posts(all_posts)

    return "Post was Successfully deleted."

#End of my own code


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

# Gregs Code Starts Here


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
