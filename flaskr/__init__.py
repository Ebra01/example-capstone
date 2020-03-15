from functools import wraps
from flask import Flask, jsonify, session, redirect, url_for, render_template, request
from flask_cors import CORS
from flaskr.models.models import setup_db, db
import flaskr.auth.auth as auth
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import json

user = False

DOMAIN = 'fsnd-capstone.auth0.com'
CLIENT_ID = 'c0XAJzf9A9M6rM5jB02V7SGGbc2PLknf'
CLIENT_SECRET = 'QIhv5YFzdOBprDntk1R5Q4fmNnegMxFATmTZhWHbZBT5NJ-6Ut2Cdx7LE3KkT3dF'
AUDIENCE = 'capstone'


def create_app():
    app = Flask(__name__)

    setup_db(app)

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        api_base_url=f'https://{DOMAIN}',
        access_token_url=f'https://{DOMAIN}/oauth/token',
        authorize_url=f'https://{DOMAIN}/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS,PATCH')

        return response

    from flaskr.actors.routes import actor
    from flaskr.movies.routes import movie
    from flaskr.main.routes import main
    from flaskr.errors.handlers import errors

    app.register_blueprint(actor)
    app.register_blueprint(movie)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                # Redirect to Login page here
                return redirect('/')
            return f(*args, **kwargs)

        return decorated

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
        }

        return redirect('/dashboard')

    @app.route('/login')
    def login():
        global user

        user = True
        inject_user()

        return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback')

    @app.route('/logout')
    def logout():
        global user
        # Clear session stored data
        session.clear()

        user = False
        inject_user()

        # Redirect user to logout endpoint
        params = {'returnTo': url_for('main.home', _external=True), 'client_id': 'c0XAJzf9A9M6rM5jB02V7SGGbc2PLknf'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/dashboard')
    @requires_auth
    def dashboard():
        return render_template('pages/dashboard.html',
                               userinfo=session['profile'],
                               userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

    @app.context_processor
    def inject_user():
        return dict(user=user)
    return app
