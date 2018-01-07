from django.db import models

# Create your models here.


class State(models.Model):
    """
    Model to describe a state
    """
    name = models.CharField(max_length=128)
    abbrev = models.CharField(max_length=2)
    capital = models.CharField(max_length=128)
    fips_code = models.SmallIntegerField()


class City(models.Model):
    """
    This model describes a city
    """
    city_name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class Subscriber(models.Model):
    """
    This database model describes the subscriber
    """
    email = models.EmailField()
    is_valid = models.BooleanField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
