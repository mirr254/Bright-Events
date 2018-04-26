# Bright Events

![travis build](https://travis-ci.org/mirr254/Bright-Events.svg?branch=development) [![Coverage Status](https://coveralls.io/repos/github/mirr254/Bright-Events/badge.svg?branch=development)](https://coveralls.io/github/mirr254/Bright-Events?branch=development) [![Maintainability](https://api.codeclimate.com/v1/badges/113acdcc6ca3deff6f20/maintainability)](https://codeclimate.com/github/mirr254/Bright-Events/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/113acdcc6ca3deff6f20/test_coverage)](https://codeclimate.com/github/mirr254/Bright-Events/test_coverage)

## Description
Bright events provides a platform for event organizers to create and manage different types of events while making them easily accessible to target markets.

## Functionalities
- Users can create account and log in
- Users can create, view, update and delete an event
- Users can RSVP to an event - Users can respond to events
- Users can view who will be attending their event
- Users can search for events based on event location or event category

This is a web application implemented in python

The API can be accessed from [Brighter-events Api](https://brighter-event.herokuapp.com/)

The app skeleton to be integrated with API can be accessed through github pages found at [Brighter Events homepage](https://mirr254.github.io/)

## Installation
- Clone the repo 
[Clone](https://github.com/mirr254/Bright-Events.git)
- Change directoy

  `cd Bright-Events`
-Create a virtue enviroment to work on
 `virtualenv -p python3 <name>`

- Activate the virtue enviroment

  `source <name>/scripts/activate `

- Install the dependancies

  `pip install -r requirements.txt`

## Tests

Running all tests via nosetests. Wil perform tests on the tests folder

`nosetests tests/`

## Running the app

`python run.py`

# Designs documentation.
Bright events will basically have 3 classes. User, Events and SharedEvents. Shared events will track who shared an event with who. This will assist when users are viewing events and they can see the events they have been invited and make an RSVP to them with either attending,maybe, not attending.

The application's entry point is to be the login page. Where both login and registration have been put in the same page but separated by tabs. 
This will help maintain user concentration and won't give users alot of work to navigate from page to page. The entry point is as shown in the image below.

## Login

![Login](/Designs/documentation-imags/login.PNG)

## Registration

![Registration](/Designs/documentation-imags/register.PNG)

## Main or Home page

Once the user is authenticated. He is directed to home page where he finds a list of events e has created in tabular form as shown below.

![list](/Designs/documentation-imags/viewEvents.PNG)

Within the same page a user can add and event by clicking the add event button on top of the page. Which brings pop up for to add details of the user. This again is to minimize navigation from page to page

![Add Event](/Designs/documentation-imags/newEvent.PNG)

The action column on the far right is where the edit, delete and share buttons will be located.
