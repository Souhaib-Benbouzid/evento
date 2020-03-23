from datetime import datetime
from evento import db


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
                        db.Column('person_id', db.Integer,
                                  db.ForeignKey('person.id'), unique=True),
                        db.Column('party_id', db.Integer,
                                  db.ForeignKey('party.id'), unique=True)
                        )


class Person(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)

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


class Party(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)

    invitees = db.relationship(
        'Person', secondary=person_party, backref=db.backref('parties'), lazy=True)

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
