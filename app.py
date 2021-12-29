from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

#app.add_url_rule('/', 'hello' hello_world)


@app.route('/darkness')
def darkness():
    return 'Hello darkness my old friend'


if __name__ == '__main__':
    app.run()
    app.run(debug=True)
