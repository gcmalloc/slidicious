from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import task
import json
import os
import logging

app = Flask(__name__)
application = app
app.config.update(
        BOWER_PACKAGE = ['jquery'],
        BOWER_BIN = '/home/malik/Scribble/flask_boostrap_template/node_modules/.bin/bower',
        COMPILED_DIR = "slides"
        )


@app.route('/', methods=['GET'])
def index():
    return  render_template('carousel.html', last_slides=[])

@app.route('/hook', methods=['POST'])
def github_hook():
    logging.debug(request.form.keys())
    logging.debug(request.form['payload'])
    github_data = json.loads(request.form['payload'])
    logging.debug(github_data)
    repo  = github_data["repository"]
    url = repo["url"]
    uniq_name = "/".join(url.split('/')[-2:])
    task.compile_slides.delay(url, os.path.join(os.path.join(app.static_folder, app.config['COMPILED_DIR']), uniq_name))
    return jsonify(response="OK")


if __name__ == '__main__':
    app.run(debug=True)
