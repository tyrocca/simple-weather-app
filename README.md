# simple-weather-app
### Simple Weather App for Klaviyo

This is my implementation of a simple weather email app. I built it using django 2.

## Setup

To run the code first download the repo. Then in a python 3 virtual environment run `pip -r requirements.txt`.

Next you will need to make your initial migrations so run `python manage.py makemigrations emails` then run
`python manage.py migrate emails` to create the proper tables.

Next you want to add the data to the tables. To do this run `python manage.py runscript load_grographies`. This 
command creates all of the city and state objects in the database.

## Using the application

### Client Side
With the server running (`python manage.py runserver`) one can experience the product as a customer. Navigate to 
http://localhost:8000/emails/ to view the signup page. I built the signup page using django forms and bootstrap, and then
used select2.js to make the dropdowns. Django's form email validator is one way that I tried to protect from malicious input.
If a user enters the same address multiple times this will only change the user's location.

### Server Side

On the server side I have three models:
- `Subscriber` - this model represents a subscriber. A subscriber has an email field, valid email field, a city field, and a state field. (As an extension I would have liked to make a unique key per subscriber for activating their email address, but this would have complicated me sending emails to klaviyo so I left it off. Ideally one would do this and prune emails that went unvalidated for a certain amount of time).
- `State` - this represents a subscriber's state. I made this a model (although it could have also been an enum). This object could be useful if you were trying to target a specific subset of subscribers.
- `City` - all the subscribers are tied to a city. I decided to add sending methods to this models to limit the number of requests being sent to wunderground. This way we only make a request to wunderground iff there are subscribers in that city. This makes it so we would only make a max of 100 requests to wunderground even if we had millions of subscribers.

### Sending Emails

To send emails the user needs to send by running `python manage.py runscript send_emails`. This will send emails to all of the
validated users. We only make one request per city and generate the email text once per city to be as efficient as possible. If we were scaling this up we could even use threads. I had to make a throwaway gmail account for sending these emails, but ideally I would have used an email service like sparkpost and done my substitutions through them. For the email html I used a template tool www.beefree.io. This is a plugin tool that I used at www.quorum.us to build their email tool. It does a nice job of handling different browsers.

### Simple Improvements that would make this more fun to use
- Embedding a drag-and-drop tool for clients to use to generate their own email. Allowing them to use more variables in their emails would be cool
- Making this a single page application with react/redux. This application had no need for all of the boilerplate, but if you were building this out into a more fully featured tool that would be nice
- Email unsubscribe feature - generate per subscriber hash that connects to a view that lets them unsubscribe
- Email tracking analytics - it is easy to embed a 1x1 pixel to track opens, or use a service like sparkpost to do this.
