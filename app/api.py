from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_debugtoolbar import DebugToolbarExtension

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'joe', 'pass'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
print username_table, userid_table

def authenticate(username, password):
    print 'auth argvs:', username, password
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    print 'payload:', payload
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secretYF(@EH*Hjosdfo'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
# app.config['JWT_AUTH_PASSWORD_KEY'] = 'password'

jwt = JWT(app, authenticate, identity)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return '<body>Welcome, %s</body>' % current_identity

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
