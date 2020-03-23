
import bleach

from datetime import datetime
from flask import request, abort, jsonify, redirect, render_template, url_for, flash

from evento.auth import requires_auth, AuthError
from evento import app, db
from evento.models import Party, Person


# *******************************************************               ROUTES                  *********************************************************

@app.route('/', methods=['GET'])
def index():
    return "Evento API"


#******************************    Party     **************************************#
@app.route('/parties/', methods=['GET'])
def parties():
    try:
        parties = Party.query.all()

        if parties:
            return jsonify({
                'parties': [{party.name: party.state} for party in parties],
                'number of parties': len(parties),
                'success': True,
            }), 200
        else:
            return jsonify({
                'success': True,
                'number of parties': 0,
                'parties': [],
            }), 200
    except:
        abort(404)


@app.route('/parties/display', methods=['GET'])
@requires_auth('read:details')
def party(payload):
    try:
        party = Party.query.filter_by(name=request.get_json()['name']).first()
        return jsonify({
            'party': party.format(),
            'success': True,
        }), 200
    except:
        abort(404)


@app.route('/parties/add', methods=['POST'])
@requires_auth('create:party')
def add_party(payload):
    try:
        party = Party.query.filter_by(
            name=bleach.clean(request.get_json()['name'])).first()
        if party:
            abort(409)
        # sanitize inputs and store
        party = Party(name=bleach.clean(request.get_json()['name']), description=bleach.clean(
            request.get_json()['description']), date=request.get_json()['date'], state=request.get_json()['state'], city=request.get_json()['city'])
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
        party = Party.query.filter_by(name=request.get_json()['name']).first()
        # data insert
        if party:
            if request.get_json().get('name_change'):
                party.name = bleach.clean(request.get_json().get('name_change'))

            if request.get_json().get('description'):
                party.description = bleach.clean(
                    request.get_json().get('description'))
            if request.get_json().get('date'):
                party.date = datetime.strptime(
                    request.get_json().get('date'), '%Y-%m-%d %H:%M:%S')
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
        party = Party.query.filter_by(name=request.get_json().get('name')).first()
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
                'invitees': [{person.name: person.email} for person in invitees],
                'number of invites': len(invitees),
                'success': True,
            }), 200
        else:
            return jsonify({
                'success': True,
                'number of invites': 0,
                'invitees': [],
            }), 200
    except:
        abort(404)


@app.route('/invitees/display', methods=['GET'])
@requires_auth('read:invitees_details')
def invities_display(payload):
    try:
        invitees = Person.query.filter_by(name=request.get_json()['name']).first()
        return jsonify({
            'invitees': invitees.format(),
            'success': True,
        }), 200
    except:
        abort(404)


@app.route('/invitees/add', methods=['POST'])
@requires_auth('add:invitees')
def add_invities(payload):
    try:
        invitees = Person.query.filter_by(
            name=bleach.clean(request.get_json()['name'])).first()
        if invitees:
            abort(409)
        # sanitize inputs and store
        invited = Person(name=bleach.clean(request.get_json()['name']), email=bleach.clean(
            request.get_json()['email']), phone=bleach.clean(request.get_json()['phone']))
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
        invitees = Person.query.filter_by(name=request.get_json()['name']).first()
        # data insert
        if invitees:
            if request.get_json().get('name_change'):
                invitees.name = bleach.clean(request.get_json().get('name_change'))
            if request.get_json().get('email'):
                invitees.email = bleach.clean(request.get_json().get('email'))
            if request.get_json().get('phone'):
                invitees.phone = bleach.clean(request.get_json().get('phone'))

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
        invitees = Person.query.filter_by(
            name=request.get_json().get('name')).first()
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
        invitees = Person.query.filter_by(
            email=bleach.clean(request.get_json()['invitee_email'])).first()
        party = Party.query.filter_by(
            name=bleach.clean(request.get_json()['party_name'])).first()
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
        party = Party.query.filter_by(
            name=bleach.clean(request.get_json()['party_name'])).first()
        invitees = Person.query.filter_by(
            email=bleach.clean(request.get_json()['invitee_email'])).first()
        if not party:
            abort(404)
        if not invitees:
            abort(404)

        party.invitees.remove(invitees)
        db.session.commit()
        return jsonify({
            'description': f"{request.get_json()['invitee_email']} deleted from the party!.",
            'success': True,
        }), 200

    except:
        db.session.rollback()
        abort(404)


@app.route('/parties/invitees', methods=['GET'])
@requires_auth('read:invitees_details')
def party_invitees(payload):
    try:
        party = Party.query.filter_by(
            name=bleach.clean(request.get_json()['party_name'])).first()
        if party:
            return jsonify({
                'party': party.name,
                'invitees': [{person.name: person.email} for person in party.invitees],
                'number of invites': len(party.invitees),
                'success': True,
            }), 200
        else:
            return jsonify({
                'party': party.name,
                'success': True,
                'number of invites': 0,
                'invitees': [],
            }), 200
    except:
        abort(404)

# *******************************************************               Erors                  *********************************************************


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'description': 'Resources Not Found',
        'status': 404
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'description': 'Something went wrong',
        'status': 500
    }), 500


@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        'success': False,
        'description': 'Unauthorized, Permission not found',
        'status': 403
    }), 403


@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({
        'success': False,
        'description': 'Unauthorized, Permission not found',
        'status': 403
    }), 403


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
