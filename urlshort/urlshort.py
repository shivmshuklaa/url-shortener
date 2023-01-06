import json
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from os import path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)


@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)

        if request.form['code'] in urls.keys():
            flash("short name is already been taken")
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form["code"]] = {'url': request.form["url"]}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(
                'C:/Users/SHIVAM SHUKLA/projects/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form["code"]] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form["code"]] = True
        return render_template('your_url.html', code=request.form["code"])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    if path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('urlshort.static', filename='user_files/' + urls[code]['file']))
    return abort(404, 'Oops! didn\'t found what you are looking for')


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == '__main__':

    bp.run(debug=True)
