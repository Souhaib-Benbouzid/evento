import os
import unittest
import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from evento import app, db


class TestApi(unittest.TestCase):

    def setUp(self):
        self.host_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEJOVVZFT0RkRE1VRkdRVEJCT0RBeU1FSkZNa1UwTkVSRFFUbERSRVkzTVVKRk9VUkVNQSJ9.eyJpc3MiOiJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NDE2MDk5NDI2ODc5NjQ2MTQzIiwiYXVkIjpbIlBhcnR5TGFuZF9BcGkiLCJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NDk1OTk0OCwiZXhwIjoxNTg1MDMxOTQzLCJhenAiOiJoWW4xdFptVWZMd2NHMlJ5eTA4ZGpYTDBkZXpRWFZsSCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6aW52aXRlZXMiLCJjcmVhdGU6cGFydHkiLCJkZWxldGU6aW52aXRlZXMiLCJkZWxldGU6cGFydHkiLCJyZWFkOmRldGFpbHMiLCJyZWFkOmludml0ZWVzX2RldGFpbHMiLCJ1cGRhdGU6aW52aXRlZXMiLCJ1cGRhdGU6cGFydHkiXX0.J7PYEUVceXTKfPWIPDdUKOkZ_CoxRDnNMR0YMZArlJzmxFW52WKs6HBxqPbCcD74EU118TNFGVjz1HlmOTKBQJITJg9CGpJB1J3lUHsRl5i6QfAGbXyGDGCq0IHBDYzAvpryPkQHDK5zzvk2PBq0cCE9FnEjHsfL7C_R-YGjTrYQLDVFsuYK0gY6p35nirNkvBaDy-5-iSHtJZd9g3ba70xo83ymU-mf8CpwEkOEfsQzpZBnwhqJoTqX7ly3r_1tnvD1UXtVhHe-F3Eg5O0aNrs7VcS8rbog5uMtx-mKgAc34Hb7TBl6CuasXtzFKNfOipEqJKW-ZzzMWgTL0TqQSQ'

        self.invitee_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEJOVVZFT0RkRE1VRkdRVEJCT0RBeU1FSkZNa1UwTkVSRFFUbERSRVkzTVVKRk9VUkVNQSJ9.eyJpc3MiOiJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEyODU5MjIxOTk4MTI1NzQ4NzM5IiwiYXVkIjpbIlBhcnR5TGFuZF9BcGkiLCJodHRwczovL3NvdWhhaWJiZW5ib3V6aWQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NDg5MTIzNywiZXhwIjoxNTg0OTYzMjMyLCJhenAiOiJoWW4xdFptVWZMd2NHMlJ5eTA4ZGpYTDBkZXpRWFZsSCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmRldGFpbHMiLCJyZWFkOmludml0ZWVzX2RldGFpbHMiXX0.Of1IXfPlr68R0oyI8DXn-t29GUgoCN20v28w6i7WzxoMzzQBVlkwjXiM1l8swK0EyJtNI5o87b6OPGPv3rZNc6pstylfxZesQmJ0YMREKQFgRLyzWKoUiPQyysJAUGhCe8P_nWlOh57BAFCTdYQDIdKsv-qIAFBcPJICwL03PjlGT8-E757tbkXMBMF3DmO3f55tdO4Mz7vSi_OGvAzK5T62oASJd6q94-EnrYhwI92d6uo5laHoKelRkqib6vD2DzQ41_EA6Ve_yvyJjWLEr9iQ0UB33lSW-GKgKY4uJgspjBf4nZFUb1GLYHh_Slr4kHPsSCVMZbgYtwC1nu22Ag'

        self.party = {
            "name": "mando",
            "description": "for fun",
            "date": "2020-02-21 12:12:12",
            "city": "New York",
            "state": "NY"
        }


        self.invitee = {
            'name': 'souhaib',
            'email': 'souhaib@gmail.com',
            'phone': '123-123-1234'
        }

        """ Define test variables and initialize app."""
        self.app = app

        # init client
        self.client = self.app.test_client

        # setup db
        self.db = SQLAlchemy(self.app)
        self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Endpoint : /parties/add
    # party tests

    def test_add_party_host(self):
        response = self.client().post('/parties/add',
                                      json=self.party,
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['description'],
                         f"Party {self.party['name']} is ready to Rock !!!")

    def test_add_party_invited(self):
        response = self.client().post('/parties/add',
                                      json=self.party,
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_add_party_not_invited(self):
        response = self.client().post('/parties/add',
                                      json=self.party,
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    # Endpoint : /parties

    def test_get_parties_host(self):
        response = self.client().get('/parties/',
                                     headers={"Authorization": self.host_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_parties_invited(self):
        response = self.client().get('/parties/',
                                     headers={"Authorization": self.invitee_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #not invited

    def test_get_parties_not_invited(self):
        response = self.client().get('/parties/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)



    # Endpoint : /parties/update

    def test_update_party_host(self):
        response = self.client().patch('/parties/update',
                                      json={"name": "Jazz time", "description":" new description"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['description'])

    def test_update_party_invited(self):
        response = self.client().patch('/parties/update',
                                      json={"name":"Jazz time", "description":" new description"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_party_not_invited(self):
        response = self.client().patch('/parties/update',
                                      json={"name":"Jazz time", "description":" new description"},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)


    # Endpoint : /parties/delete

    def test_delete_party_host(self):
        response = self.client().delete('/parties/delete',
                                      json={"name": self.party['name']},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['description'])

    def test_delete_party_invited(self):
        response = self.client().delete('/parties/delete',
                                      json={"name": self.party['name']},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_party_not_invited(self):
        response = self.client().delete('/parties/delete',
                                      json={"name": self.party['name']},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)




    # Endpoint : /invitees/add
    # invitee tests

    def test_add_invitee_host(self):
        response = self.client().post('/invitees/add',
                                      json=self.invitee,
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
       

    def test_add_invitee_invited(self):
        response = self.client().post('/invitees/add',
                                      json=self.invitee,
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_add_invitee_not_invited(self):
        response = self.client().post('/invitees/add',
                                      json=self.invitee,
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    # Endpoint : /invitees

    def test_get_invitee_host(self):
        response = self.client().get('/invitees/',
                                     headers={"Authorization": self.host_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_invitee_invited(self):
        response = self.client().get('/invitees/',
                                     headers={"Authorization": self.invitee_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
    #not invited

    def test_get_invitee_not_invited(self):
        response = self.client().get('/invitees/')
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)



    # Endpoint : /invitees/update

    def test_update_invitee_host(self):
        response = self.client().patch('/invitees/update',
                                      json={"name": "souhaib", "name_change":"souhaibos", "email":"sdasas@gmail.com", "phone":"321-654-6547"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               },)
        data = response.get_json()
       
        self.assertEqual(response.status_code, 400)

    def test_update_invitee_invited(self):
        response = self.client().patch('/invitees/update',
                                      json={"name": self.invitee['name'], "email":"test@gmail.com"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_invitee_not_invited(self):
        response = self.client().patch('/invitees/update',
                                      json={"name": self.invitee['name'], "email":"test@gmail.com"},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)


    # Endpoint : /invitees/delete

    def test_delete_invitee_host(self):
        response = self.client().delete('/invitees/delete',
                                      json={"name": self.invitee['name']},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['description'])

    def test_delete_invitee_invited(self):
        response = self.client().delete('/invitees/delete',
                                      json={"name": self.invitee['name']},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_invitee_not_invited(self):
        response = self.client().delete('/invitees/delete',
                                      json={"name": self.invitee['name']},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)




# Endpoint /parties/invitees/add


    def test_add_invitee_to_party_host(self):
        response = self.client().post('/parties/invitees/add',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
       

    def test_add_invitee_to_party_invited(self):
        response = self.client().post('/parties/invitees/add',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_add_invitee_to_party_not_invited(self):
        response = self.client().post('/parties/invitees/add',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)


# Endpoint /parties/invitees/delete


    def test_delete_invitee_from_party_host(self):
        response = self.client().delete('/parties/invitees/delete',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.host_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['description'])

    def test_delete_invitee_from_party_invited(self):
        response = self.client().delete('/parties/invitees/delete',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json",
                                               "Authorization": self.invitee_token,
                                               },)
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_invitee_from_party_not_invited(self):
        response = self.client().delete('/parties/invitees/delete',
                                      json={"invitee_email":"souhaib@gmail.com", "party_name":"Jazz time"},
                                      headers={"Content-Type": "aplication/json"})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)



# Endpoint /parties/invitees

    def test_get_invitee_host(self):
        response = self.client().get('/parties/invitees',
                                        json={'party_name':'Jazz time'}
                                     headers={"Authorization": self.host_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_invitee_invited(self):
        response = self.client().get('/parties/invitees',
                                        json={'party_name':'Jazz time'}
                                     headers={"Authorization": self.invitee_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
    #not invited

    def test_get_invitee_not_invited(self):
        response = self.client().get('/parties/invitees',
                                        json={'party_name':'Jazz time'})
        data = response.get_json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
