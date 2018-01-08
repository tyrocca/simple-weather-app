import requests
from django.db import models
from django.conf import settings

# Create your models here.
weather_root_url = "http://api.wunderground.com/api/"


class State(models.Model):
    """
    Model to describe a state
    """
    name = models.CharField(max_length=128)
    abbrev = models.CharField(max_length=2)
    capital = models.CharField(max_length=128)
    fips_code = models.SmallIntegerField()

    def __str__(self):
        return self.name


class City(models.Model):
    """
    This model describes a city
    """
    city_name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        ordering = ["city_name"]

    def __str__(self):
        return "{}, {}".format(self.city_name, self.state.abbrev)

    ######################################
    # Methods for processing the weather #
    ######################################
    def _get_weather_url(self):
        """ Creates the request string"""
        return "{base_url}{key}/almanac/conditions/q/{state}/{city}.json".format(
            base_url=weather_root_url,
            key=settings.WUNDERGROUND_API_KEY,
            state=self.state.abbrev,
            city=self.city_name.replace(" ", "_"),
        )

    def get_weather(self):
        """
        This method returns the average weather and current weather for a
        given city (as long as the city has subscribers)
        """
        results = {}
        # if no people subscribe, then don't send a request (as we are limited)
        if self.subscriber_set.exists() is False:
            return results
        # get the weather
        r = requests.get(self._get_weather_url()).json()

        # if not a valid response, return the empty object
        if not r or "response" not in r or \
                "almanac" not in r or \
                "current_observation" not in r:
            return results

        # set the average
        results["avg_high"] = int(r["almanac"]["temp_high"]["normal"]["F"])
        results["avg_low"] = int(r["almanac"]["temp_low"]["normal"]["F"])

        # set the current
        results["current_weather"] = r["current_observation"]["weather"]
        results["current_temp"] = float(r["current_observation"]["temp_f"])
        results["temp_string"] = r["current_observation"]["temperature_string"]
        results["feels_like"] = r["current_observation"]["feelslike_string"]
        results["icon"] = r["current_observation"]["icon"]
        results["icon_url"] = r["current_observation"]["icon_url"]

        # return a dictionary containing all the info
        return results

    def make_subject(self, report):
        """ Method that creates the email subject given a report """
        subject = "Enjoy a discount on us"
        if not report:
            return subject
        elif report["current_weather"].lower() == "sunny" or \
                report["current_temp"] >= (report["avg_high"] + 5):
            subject = "It's nice out! " + subject
        elif report["icon"].lower() == "rain" or \
                report["current_temp"] <= (report["avg_low"] - 5):
            subject = "Not so nice out? That's okay, enjoy a discount on us."
        return subject

    def make_body(self, report):
        """ method that constructs the html of the email"""
        body = ""
        with open("./scripts/email.html") as f:
            body = f.read().replace('\n', '')

        # if I was using an email service like sparkpost or mailgun
        # I would use their substitution dictionary
        body = body.replace("{{icon_url}}", report.get("icon_url", ""))
        body = body.replace("{{icon}}", report.get("icon", ""))
        body = body.replace("{{location}}", report.get("location", ""))
        body = body.replace("{{feels_like}}", report.get("feels_like", "N/A"))
        body = body.replace("{{current_weather}}",
                            report.get("current_weather", "N/A"))
        body = body.replace("{{current_temp}}",
                            report.get("temp_string", "N/A"))

        return body

    def make_plaintext(self, report):
        """ method that generates the email plaintext """
        return "The weather in {} is {}. It feels like {}".format(
            report.get("location", "your town"),
            report.get("temp_string", "N/A"),
            report.get("feels_like", "N/A"),
        )

    def generate_email(self):
        """ Function to generate an email"""
        report = self.get_weather()
        subject = self.make_subject(report)
        body = self.make_body(report)
        plaintext = self.make_plaintext(report)
        return subject, body, plaintext


class Subscriber(models.Model):
    """
    This database model describes the subscriber
    """
    email = models.EmailField()
    is_valid = models.BooleanField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.email if self.is_valid \
            else "Invalid: {}".format(self.email)
