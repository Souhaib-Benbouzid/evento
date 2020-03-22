## Evento 

Evento is a an event manager app,find events in your area!. or publisize your own event!
in evento you can easily list an event! invite people to your event. and manage your invitations smoothly. 
you dont have an event?. You can attend events in your area! and search for people that have similar interests.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database

you need PostgreSQL + 10.x
create a database

```bash
psql createdb app
```

create the models

```bash

python 

from app import db

db.create_all()

```


#### Running the server

navigate to the app folder

```bash
python app.py
```

#### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API


## API Documentation 

currently the api is underdevelopment and only run on localhost.

#### API ENDPOINTS
Base URL : https://evento13.herokuapp.com

##### GET /parties

return list of parties,array of party objects {party name : party place} 

response example

{
  "number of parties": 1,
  "parties": [
    {
      "Jazz time": "california"
    }
  ],
  "success": true
}

##### GET /invitees

return list of invitees,array of invitees objects {invitee name : invitee email} 

response example

{
  "invitees": [
    {
      "souhaib": "souhaib@gmail.com"
    }
  ], 
  "number of invites": 1, 
  "success": true
}


##### GET /parties/display

return party details

response example

{
  "party": {
    "city": "los angeles ",
    "date": "Wed, 01 Apr 2020 19:00:00 GMT",
    "description": "lets have a smoth night",
    "id": 1,
    "name": "Jazz time",
    "state": "california"
  },
  "success": true
}


##### GET /invitees/display

return invitees details

response example

{
  "invitees": {
    "email": "souhaib@gmail.com",
    "id": 1,
    "name": "souhaib",
    "phone": "123-123-1234"
  },
  "success": true
}

##### GET /parties/invitees

return list of invitees in a party

response example

{
  "invitees": [
    {
      "souhaib": "souhaib@gmail.com"
    }
  ],
  "number of invites": 1,
  "success": true
}


##### POST /parties/add


add a party, return a success status and description includes the name of the party

response example

{
  "description": "Party Jazz time is ready to Rock 🤘 !!! ",
  "success": true
}

##### POST /invitees/add


add an invitee, return a success status and description includes the name of the invitee

response example

{
  "description": "Invitee souhaib is ready to Rock 🤘 !!! ",
  "success": true
}

##### POST /parties/invitees/add


add an invitee to a party, return a success status and description includes the name of the invitee and the party name

response example

{
  "description": "Invitee souhaib is added to the Jazz time !!! ",
  "success": true
}



##### DELETE /parties/delete


delete a person, return a success status and description

response example

{
  "description": "Party deleted!. :[ ",
  "success": true
}

##### DELETE /invitees/delete


delete a person, return a success status and description

response example

{
  "description": "Person deleted!. :[ ",
  "success": true
}

##### DELETE /parties/invitees/delete

Delete an invitee from a party, return a success status and description includes the name of the invitee and the party name

response example

{
  "description": "souhaib@gmail.com deleted from the party!.",
  "success": true



##### PATCH /parties/update

update an invitee details, return a success status and description 

response example

{
  "description": "My party parameters has been updated successfully!. Bip Bop",
  "success": true
}




