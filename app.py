import sqlite3, os, json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# Create application and db config
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'post.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-carpool-list', methods=['GET'])
def get_post():
    print request.args.get('from'), request.args.get('to')

    from_loc = request.args.get('from').strip().lower()
    to_loc = request.args.get('to').strip().lower()

    db = get_db()
    cur = db.execute('SELECT * FROM post WHERE lower(origin) = \'%s\' AND lower(destination) = \'%s\'' % (from_loc, to_loc))

    data = cur.fetchall()

    # Create JSON return file
    json_return = {'result': []}
    for x in data:
        json_return['result'].append(dict(zip(['id','origin','destination'], x)))
    return json.dumps(json_return)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'post.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


if __name__ == '__main__':
    app.run(debug=True,port=8000)
