# Busie Flask Helper

A package to help with common initialization code across Busie Flask projects

Helpful for use with the application factory pattern.
Allows for modularization of initialization code, such that factories are not cluttered with boilerplate initialization

## Installation

`pip install busie-flask-helper`

## Usage

```python
# in app.py, or wherever application initialization lives
from busie_flask import FlaskHelper
helper = FlaskHelper('abs/path/to/project/')
db = helper.db
auth = helper.auth
cache = helper.cache

# Other Initialization Code omitted

def create_app():
    app = Flask(__name__)
    # Other App Factory initialization omitted

    # this invocation initializes all of the helper objects with the application
    # this includes migration commands, models, views, auth, cache client, orm
    helper.init_app(app, 'relative/path/to/models', '/relative/path/to/views')

    return app

# in some module, maybe an API View
from flask import request, render_template
from src.app import auth, app

@app.route('/foo')
@auth.requires_web_auth
def foo():
    return render_template('foo.html')

class SomeView(MethodView):
    decorators = [auth.require_api_auth]

    def get(self):
        if auth.requires_permission('SomeView:bar'):
            return 'ok', 200
        raise AuthError({'code': 'some_error', 'description': 'something went wrong'}, 403)
```

## API

### FlaskHelper

#### Public Properties
* `db` <[SQLAlchemy] (https://flask-sqlalchemy.palletsprojects.com/en/2.x/)>
* `auth` <[AuthHelper] (#authhelper)>
* `cache` <[CacheClient] (#cacheclient)>

#### Public Methods
* `FlaskHelper(root_dir, app=None, models_dir=None, views_dir=None)`
    * param `root_dir`: The root directory of the project, best practice to pass an abspath here. if your application lives in src/app then your root dir should be src/
    * See `init_app` method documentation for specifics on the other params
* `init_app(self, app, models_dir, views_dir)`
    * param `app`: A Flask application instance
    * param `models_dir`: Relative path to the models directory, with respect to the root_dir that the helper was initialized with
    * param `views_dir`: same as `models_dir`, but for views


### AuthHelper
This is an Auth0 Integration. It comes with helpful decorators for protecting both API and Web App views. It also automatically adds `/login`, `/callback`, and `/logout` routes to your application for Auth0 Authorization Code Flow Authentication. Note that this feature cannot be disabled at this time, but this ability will be added in a future release. In web applications and API's, merely authenticating should *never* be enough to gain access to a protected resource. 

#### Public Properties
**None**

#### Public Methods
* `AuthHelper(app=None)`: Constructor
* `init_app(self, app)`: Initialize the AuthHelper with a Flask application
    * param `app`: A Flask application instance. app.config _must_ have `AUTH0_AUDIENCE` `AUTH0_DOMAIN` and `AUTH0_ALGORITHMS`
* `requires_api_auth(self, f)`: A decorator for views that require the auth code with pkce flow.
* `requires_web_auth(self, f)`: A decorator for views that require the auth code flow (no pkce)
* `get_rsa_key_from_unverified_token(self, token)`: Determines the RSA key to use from the token's `kid`
    * param `token`: A json web token with appropriate headers
    * return: `rsa_key (dict)` or `None`
* `handle_rsa_decode(self, rsa_key, token)`: decodes the token using rsa
    * param `rsa_key`: dict representation of an RSA key
    * param `token`: a json web token with necessary claims
* `requires_scope(self, required_scope)`: determine if the auth token has the provided required scope
    * param `required_scope`: string, the desired scope for the resource
    * return: `bool`
* `requires_permission(self, required_permission)`: determine if the auth token has the provided required permission
    * param `required_permission`: string, the desired permission for the resource
    * return: `bool`
* `static -> get_token_auth_header()`: gets the auth header from the request context and formats it properly
    * return: `str`

### CacheClient

#### Public Properties
* `redis`: The redis instance. Allows for direct interation with the python Redis API

#### Public Methods
* `CacheClient(app=None)`: Constructor
* `init_app(self, app)`: Initialize the redis client with application.
    * param `app`: A Flask application instance. app.config _must_ have `REDIS_HOST` `REDIS_PORT` and `REDIS_DB`. **NOTE** `REDIS_PASSWORD` is also used, but this method _will not_ throw without it
* `get`: Alias for redis.get
* `set`: Alias for redis.set
 
