import os
import unittest
import json

from evento import create_app
from flask_sqlalchemy import SQLAlchemy


class Party_Invitees_Tests(unittest.TestCase):

    def setUp(self):
        """ Define test variables and initialize app."""
        self.app = create_app()

        #  config app
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DATABASE_URL')

        # init client
        self.client = self.app.test_client

        # setup db
        self.db = SQLAlchemy(app)
        self.db.create_all()

        # setup data
        self.party = {
            'name': 'Jazz time',
            'description': 'Chill night in LA',
            'date': '2020-04-01 19:00:00',
            'city': 'Los Angeles',
            'state': 'California'
        }

        self.invitee = {
            'name': 'souhaib',
            'email': 'souhaib@gmail.com',
            'phone': '123-123-1234'
        }

        self.host_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEJOVVZFT0RkRE1VRkdRVEJCT0RBeU1FSkZNa1UwTkVSRFFUbERSRVkzTVVKRk9VUkVNQSJ9.eyJpc3MiOiJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NDE2MDk5NDI2ODc5NjQ2MTQzIiwiYXVkIjpbIlBhcnR5TGFuZF9BcGkiLCJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NDk1OTk0OCwiZXhwIjoxNTg1MDMxOTQzLCJhenAiOiJoWW4xdFptVWZMd2NHMlJ5eTA4ZGpYTDBkZXpRWFZsSCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6aW52aXRlZXMiLCJjcmVhdGU6cGFydHkiLCJkZWxldGU6aW52aXRlZXMiLCJkZWxldGU6cGFydHkiLCJyZWFkOmRldGFpbHMiLCJyZWFkOmludml0ZWVzX2RldGFpbHMiLCJ1cGRhdGU6aW52aXRlZXMiLCJ1cGRhdGU6cGFydHkiXX0.J7PYEUVceXTKfPWIPDdUKOkZ_CoxRDnNMR0YMZArlJzmxFW52WKs6HBxqPbCcD74EU118TNFGVjz1HlmOTKBQJITJg9CGpJB1J3lUHsRl5i6QfAGbXyGDGCq0IHBDYzAvpryPkQHDK5zzvk2PBq0cCE9FnEjHsfL7C_R-YGjTrYQLDVFsuYK0gY6p35nirNkvBaDy-5-iSHtJZd9g3ba70xo83ymU-mf8CpwEkOEfsQzpZBnwhqJoTqX7ly3r_1tnvD1UXtVhHe-F3Eg5O0aNrs7VcS8rbog5uMtx-mKgAc34Hb7TBl6CuasXtzFKNfOipEqJKW-ZzzMWgTL0TqQSQ'

        self.invitee_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEJOVVZFT0RkRE1VRkdRVEJCT0RBeU1FSkZNa1UwTkVSRFFUbERSRVkzTVVKRk9VUkVNQSJ9.eyJpc3MiOiJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEyODU5MjIxOTk4MTI1NzQ4NzM5IiwiYXVkIjpbIlBhcnR5TGFuZF9BcGkiLCJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NDg5MTIzNywiZXhwIjoxNTg0OTYzMjMyLCJhenAiOiJoWW4xdFptVWZMd2NHMlJ5eTA4ZGpYTDBkZXpRWFZsSCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmRldGFpbHMiLCJyZWFkOmludml0ZWVzX2RldGFpbHMiXX0.Of1IXfPlr68R0oyI8DXn-t29GUgoCN20v28w6i7WzxoMzzQBVlkwjXiM1l8swK0EyJtNI5o87b6OPGPv3rZNc6pstylfxZesQmJ0YMREKQFgRLyzWKoUiPQyysJAUGhCe8P_nWlOh57BAFCTdYQDIdKsv-qIAFBcPJICwL03PjlGT8-E757tbkXMBMF3DmO3f55tdO4Mz7vSi_OGvAzK5T62oASJd6q94-EnrYhwI92d6uo5laHoKelRkqib6vD2DzQ41_EA6Ve_yvyJjWLEr9iQ0UB33lSW-GKgKY4uJgspjBf4nZFUb1GLYHh_Slr4kHPsSCVMZbgYtwC1nu22Ag'

    def tearDown(self):
        """Executed after reach test"""
        pass


    # party tests

    def test_get_party(self):
        """TEST: Host add party  """
        res = self.client().get('/parties')
        data = res.get_json()
        self.assertEqual(data['success'] , True)
        self.assertTrue(data['description'])
        self.assertEqual(res.status_code, 200)



# Make the tests conveniently executable
if __name__ == "__main__":
unittest.main()
