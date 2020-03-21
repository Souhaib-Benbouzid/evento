import os
import json
import secrets 
import bleach
from datetime import datetime

from flask import Flask, request, abort, jsonify, redirect,render_template,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from functools import wraps
from jose import jwt
from urllib.request import urlopen

from forms import PartyForm, PersonForm

# *******************************************************               Initialazation                  *********************************************************

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
 
  return app

app = create_app()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

db.create_all()


   
# *******************************************************               Models                  *********************************************************


class Crud():
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


person_party = db.Table('person_event',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), unique= True),
    db.Column('party_id', db.Integer, db.ForeignKey('party.id'), unique= True)
)


class Person(db.Model, Crud):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True , nullable = False)
    email = db.Column(db.String(255), unique = True , nullable = False)
    phone = db.Column(db.String(255), unique = True, nullable = False)
    
    def format(self):
      person = {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone
      }
      return person

    def __repr__(self):
      return f'Party: {self.name}, {self.email}, {self.phone}'


class Party(db.Model,Crud):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    description = db.Column(db.String(500), nullable = False)
    date = db.Column(db.DateTime, nullable=False , default = datetime.utcnow)
    state = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)

    invitees = db.relationship('Person', secondary=person_party, backref=db.backref('parties'), lazy=True)

    def format(self):
        party = {
          'id': self.id,
          'name': self.name,
          'description': self.description,
          'date': self.date,
          'state': self.state,
          'city': self.city,
        }
        return party

    def __repr__(self):
      return f'Party: {self.name}, {(self.date - datetime.utcnow()).total_seconds()}'




# *******************************************************               Authentication                  *********************************************************

AUTH0_DOMAIN = 'souhaibbenbouzid.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'PartyLand_Api'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def check_permissions(permission, payload):
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission= ''):
  def requires_auth_decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
          token = get_token_auth_header()
          try:
              payload = verify_decode_jwt(token)
          except:
              abort(401)

          check_permissions(permission, payload)

          return f(payload, *args, **kwargs)

      return wrapper
  return requires_auth_decorator

# *******************************************************               ROUTES                  *********************************************************

@app.route('/', methods=['GET'])
def index():
  return render_template('pages/index.html')


#******************************    Party     **************************************#
@app.route('/parties/', methods=['GET'])
def parties():
  try:
    parties = Party.query.all()
  
    if parties: 
      return jsonify({
        'parties': [{party.name : party.state } for party in parties ],
        'number of parties' : len(parties),
        'success': True,
      }), 200
    else:
      return jsonify({
        'success': True,
        'number of parties' : 0,
        'parties': [],
      }), 200
  except :
    abort(404)
  
@app.route('/parties/display', methods=['GET'])
@requires_auth('read:details')
def party(payload):
  try:
    party = Party.query.filter_by(name=request.form['name']).first()
    return jsonify({
        'party' : party.format(),
        'success': True,
      }), 200
  except:
    abort(404)

@app.route('/parties/add', methods=['POST'])
@requires_auth('create:party')
def add_party(payload):
  try:
    party = Party.query.filter_by(name=bleach.clean(request.form['name'])).first()
    if party:
      abort(409)
    # sanitize inputs and store
    party = Party(name=bleach.clean(request.form['name']), description = bleach.clean(request.form['description']) , date = request.form['date'],state = request.form['state'],city = request.form['city'])
    party.insert()
    return jsonify({
     'success': True,
     'description': f'Party {party.name} is ready to Rock 🤘 !!! '    
    }), 200
  except:
    db.session.rollback()
    abort(400)


@app.route('/parties/update', methods=['PATCH'])
@requires_auth('update:party')
def update_party(payload):
  try:
      party = Party.query.filter_by(name=request.form['name']).first()
      # data insert
      if party: 
        if request.form.get('name_change'):
          party.name = bleach.clean(request.form.get('name_change'))
        
        if request.form.get('description'):
          party.description = bleach.clean(request.form.get('description'))
        if request.form.get('date'): 
          party.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d %H:%M:%S')
        party.update()
      
        return jsonify({
          'description': f'My party parameters has been updated successfully!. Bip Bop',
          'success': True,
        }), 200
      else:
        abort(404)
  except:
    db.session.rollback()
    abort(400)


@app.route('/parties/delete', methods=['DELETE'])
@requires_auth('delete:party')
def delete_party(payload):
  try:
    party = Party.query.filter_by(name=request.form.get('name')).first()
    if party:
      party.delete()
      return jsonify({
          'description': f'Party deleted!. :[ ',
          'success': True,
        }), 200
    else:
      abort(404)
  except:
    db.session.rollback()
    abort(500)

#******************************    Person     **************************************#

@app.route('/invitees/', methods=['GET'])
@requires_auth('read:details')
def invitees(payload):
  try:
    invitees = Person.query.all()
    if invitees: 
      return jsonify({
        'invitees': [{person.name : person.email } for person in invitees ],
        'number of invites' : len(invitees),
        'success': True,
      }), 200
    else:
      return jsonify({
        'success': True,
        'number of invites' : 0,
        'invitees': [],
      }), 200
  except:
    abort(404)
  
@app.route('/invitees/display', methods=['GET'])
@requires_auth('read:invitees_details')
def invities_display(payload):
  try:
    invitees = Person.query.filter_by(name=request.form['name']).first()
    return jsonify({
        'invitees' : invitees.format(),
        'success': True,
      }), 200
  except:
    abort(404)

@app.route('/invitees/add', methods=['POST'])
@requires_auth('add:invitees')
def add_invities(payload):
  try:
    invitees = Person.query.filter_by(name=bleach.clean(request.form['name'])).first()
    if invitees:
      abort(409)
    # sanitize inputs and store
    invited = Person(name=bleach.clean(request.form['name']), email = bleach.clean(request.form['email']),phone = bleach.clean(request.form['phone']))
    invited.insert()

    return jsonify({
     'success': True,
     'description': f'Invitee {invited.name} is ready to Rock 🤘 !!! '    
    }), 200
  except:
    db.session.rollback()
    abort(400)


@app.route('/invitees/update', methods=['PATCH'])
@requires_auth('update:invitees')
def update_invities(payload):
  try:
      invitees = Person.query.filter_by(name=request.form['name']).first()
      # data insert
      if invitees: 
        if request.form.get('name_change'):
          invitees.name = bleach.clean(request.form.get('name_change'))
        if request.form.get('email'):
          invitees.email = bleach.clean(request.form.get('email'))    
        if request.form.get('phone'):
          invitees.phone = bleach.clean(request.form.get('phone'))
      
        invitees.update()
      
        return jsonify({
          'invitees': f'My invitees parameters has been updated successfully!. Bip Bop',
          'success': True,
        }), 200
      else:
        abort(404)
  except:
    db.session.rollback()
    abort(400)


@app.route('/invitees/delete', methods=['DELETE'])
@requires_auth('delete:invitees')
def delete_invities(payload):
  try:
    invitees = Person.query.filter_by(name=request.form.get('name')).first()
    if invitees:
      invitees.delete()
      return jsonify({
          'description': f'Person deleted!. :[ ',
          'success': True,
        }), 200
    else:
      abort(404)
  except:
    db.session.rollback()
    abort(500)


#******************************    Person_Party     **************************************#


@app.route('/parties/invitees/add', methods=['POST'])
@requires_auth('add:invitees')
def add_invitees_to_party(payload):
  try:
    invitees = Person.query.filter_by(email=bleach.clean(request.form['invitee_email'])).first()
    party = Party.query.filter_by(name=bleach.clean(request.form['party_name'])).first()
    if not invitees:
      abort(404)
    if not party:
      abort(404)
    # sanitize inputs and store
    party.invitees.append(invitees)
    db.session.commit()
    return jsonify({
     'success': True,
     'description': f'Invitee {invitees.name} is added to the {party.name} !!! '    
    }), 200

  except:
    db.session.rollback()
    abort(400)


@app.route('/parties/invitees/delete', methods=['DELETE'])
@requires_auth('delete:invitees')
def delete_invities_from_party(payload):
  try:
    party = Party.query.filter_by(name=bleach.clean(request.form['party_name'])).first()
    invitees = Person.query.filter_by(email=bleach.clean(request.form['invitee_email'])).first()
    if not party:
      abort(404)
    if not invitees:
      abort(404)
    
    party.invitees.remove(invitees)
    db.session.commit()
    return jsonify({
        'description': f"{request.form['invitee_email']} deleted from the party!.",
        'success': True,
      }), 200

  except:
    db.session.rollback()
    abort(404)

@app.route('/parties/invitees', methods=['GET'])
@requires_auth('read:invitees_details')
def party_invitees(payload):
  try:
    party = Party.query.filter_by(name=bleach.clean(request.form['party_name'])).first()
    if party: 
      return jsonify({
        'party': party.name,
        'invitees': [{person.name : person.email } for person in party.invitees ],
        'number of invites' : len(party.invitees),
        'success': True,
      }), 200
    else:
      return jsonify({
        'party': party.name,
        'success': True,
        'number of invites' : 0,
        'invitees': [],
      }), 200
  except:
    abort(404)
  
# *******************************************************               Erors                  *********************************************************

@app.errorhandler(404)
def not_found_error(error):
    return jsonify( {
      'success': False,
      'description': 'Resources Not Found',
      'status': 404
    }),404

@app.errorhandler(500)
def server_error(error):
   return jsonify( {
      'success': False,
      'description': 'Something went wrong',
      'status': 500
    }),500
 
@app.errorhandler(403)
def unauthorized(error):
   return jsonify( {
      'success': False,
      'description': 'Unauthorized, Permission not found',
      'status': 403
    }),403

@app.errorhandler(AuthError)
def unauthorized(error):
   return jsonify( {
      'success': False,
      'description': 'Unauthorized, Permission not found',
      'status': 403
    }),403


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# *******************************************************               main                  *********************************************************
if __name__ == '__main__':
    app.run(port=8080, debug=True)