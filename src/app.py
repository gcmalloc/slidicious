from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import task
import json
import os
import collections
import logging

app = Flask(__name__)
app.config.from_object('src.config')
application = app

Slide = collections.namedtuple('Slide', ['author', 'file_name'])

def list_slides():
    slides_dir = os.path.join(app.static_folder, app.config['COMPILED_DIR'])
    try:
        slides_authors = os.listdir(slides_dir)
    except OSError:
        logging.warning("The directory {} doesn't exist".format(app.config['COMPILED_DIR']))
        slides_authors = []

    slides = []
    for user in slides_authors:
        user_dir = os.path.join(slides_dir, user)
        for slide in os.listdir(user_dir):
            slides.append(Slide(user, slide))
    return slides


@app.route('/', methods=['GET'])
def index():
    return  render_template('index.html', page='home')

@app.route('/slides', methods=['GET'])
def slides():
    slides = list_slides()
    return render_template('slides.html', page='slides', slides=slides)

@app.route('/hook', methods=['POST'])
def github_hook():
    logging.debug(request.form.keys())
    logging.debug(request.form['payload'])
    github_data = json.loads(request.form['payload'])
    logging.debug(github_data)
    repo  = github_data["repository"]
    url = repo["url"]
    uniq_name = "/".join(url.split('/')[-2:])
    app_args = (url, os.path.join(os.path.join(app.static_folder, app.config['COMPILED_DIR']), uniq_name))
    task.compile_slides.delay(*app_args)
    return jsonify(response="OK")


if __name__ == '__main__':
    app.run(debug=True)
