# Designs documentation.
Bright events will basically have 3 classes. User, Events and SharedEvents. Shared events will track who shared an event with who. This will assist when users are viewing events and they can see the events they have been invited and make an RSVP to them with either attending,maybe, not attending.

The UML class diagram would be as shown below

![UML](/Designs/documentation-imags/umlClassD.PNG)

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