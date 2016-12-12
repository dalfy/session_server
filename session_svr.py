from flask import Flask, g, abort, make_response
import os
import sqlite3
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database/data.db')
))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print ("Database Initialised")


def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()



@app.route('/sessions/<token>', methods=['GET'])
def get_session(token):
    db = get_db()
    json_ret = dict()

    db.execute('INSERT OR IGNORE INTO sessions (token) VALUES (?)', [token]) #Will fail if token already exist
    db.commit()
    cursor = db.execute('SELECT * FROM sessions WHERE token = ? LIMIT 1', [token])
    row = cursor.fetchall()
    if len(row) == 1:
        json_ret['session'] = {'id':    row[0][0], 'token': row[0][1]}
        return json.dumps(json_ret)
    else:
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)

