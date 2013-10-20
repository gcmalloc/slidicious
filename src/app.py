from flask import Flask
from flask import request
from flask import render_template
import task
import json

app = Flask(__name__)
app.config.update(
        BOWER_PACKAGE = ['jquery'],
        BOWER_BIN = '/home/malik/Scribble/flask_boostrap_template/node_modules/.bin/bower'
        )


@app.route('/', methods=['GET'])
def index():
    return  render_template('index.html', last_slides=[])


@app.route('/hook', methods=['POST'])
def github_hook():
    github_data = json.loads(request.form)
    repo  = github_data["repository"]
    url = repo["url"]
    task.compile_slides(url)
    return {}


if __name__ == '__main__':
    app.run(debug=True)
