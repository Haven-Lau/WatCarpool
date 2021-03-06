import sqlite3, os, json
from flask_triangle import Triangle
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# Create application and db config
app = Flask(__name__)
Triangle(app)
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


@app.route('/api/post-carpool', methods=['POST'])
def post_carpool():
    phone_number = request.form.get('phone-number').strip()
    num_spots = int(request.form.get('num-spots').strip())
    origin = request.form.get('origin').strip().lower()
    destination = request.form.get('destination').strip().lower()
    publish_date_time = request.form.get('publish-date-time').strip()
    carpool_date_time = request.form.get('carpool-date-time').strip()
    pick_up = request.form.get('pick-up').strip().lower()
    drop_off = request.form.get('drop-off').strip().lower()
    price = int(request.form.get('price'))

    print phone_number, num_spots, origin, destination, publish_date_time, carpool_date_time, pick_up, drop_off, price

    db = get_db()
    cur = db.execute('INSERT INTO post (phone_number,num_spots,origin,destination,publish_date_time,'
                     'carpool_date_time,pick_up,drop_off,price) '
                     'VALUES (\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d);'
                     % (phone_number, num_spots, origin, destination, publish_date_time, carpool_date_time,
                        pick_up, drop_off, price))
    db.commit()
    return "PLACEHOLDER"


@app.route('/api/get-carpool-list', methods=['GET'])
def get_carpool_list():
    print request.args.get('from'), request.args.get('to')

    from_loc = request.args.get('from').strip().lower()
    to_loc = request.args.get('to').strip().lower()

    db = get_db()
    cur = db.execute('SELECT * FROM post WHERE lower(origin) = \'%s\' AND lower(destination) = \'%s\'' % (from_loc, to_loc))

    data = cur.fetchall()

    # Create JSON return file
    json_return = {'result': []}
    for x in data:
        json_return['result'].append(dict(zip(['post_id', 'phone_number', 'num_spots', 'origin', 'destination',
                                               'publish_date_time', 'carpool_date_time', 'pick_up', 'drop_off',
                                               'price'], x)))
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
    app.run(debug=True, port=8000)