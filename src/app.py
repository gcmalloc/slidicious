from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import task
import json
import os

app = Flask(__name__)
application = app
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
    uniq_name = "/".join(url.split()[-2:])
    task.compile_slides(url, os.path.join(app.static_folder, uniq_name))
    return jsonify(response="OK")


if __name__ == '__main__':
    app.run(debug=True)
