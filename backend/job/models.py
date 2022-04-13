from datetime import datetime, timedelta
from http.client import NO_CONTENT
from re import L
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import geocoder
import os


def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)


# Create your models here.
class JobType(models.TextChoices):
    Permanent = ("Permanent",)
    Temporary = ("Temporary",)
    Internship = ("Internship",)


class Education(models.TextChoices):
    Bachelor = ("Bachelor",)
    Master = ("Master",)
    Phd = ("Phd",)


class Industry(models.TextChoices):
    Business = ("Business",)
    IT = ("Information Technology",)
    Banking = ("Banking",)
    Education = ("Education",)
    Telecommunications = ("Telecommunications",)
    Other = ("Other",)


class Experience(models.TextChoices):
    NO_EXPERIENCE = ("No experience",)
    ONE_YEAR = ("1 Year",)
    TWO_YEAR = ("2 Years",)
    THREE_YEAR_PLUS = ("3 Years above",)


class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100, null=True)
    jobType = models.CharField(
        max_length=10, choices=JobType.choices, default=JobType.Permanent
    )
    education = models.CharField(
        max_length=10, choices=Education.choices, default=Education.Bachelor
    )
    industry = models.CharField(
        max_length=30, choices=Industry.choices, default=Industry.Business
    )
    experience = models.CharField(
        max_length=20, choices=Experience.choices, default=Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)]
    )
    position = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=True)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    lastDate = models.DateTimeField(default=return_date_time)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key=os.getenv("GEOCODER_API"))

        print(g)

        longitude = g.lng
        latitude = g.lat

        self.point = Point(longitude, latitude)
        super(Job, self).save(*args, **kwargs)
