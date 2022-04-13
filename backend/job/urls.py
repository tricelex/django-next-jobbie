from django.urls import path
from .views import getAllJobs

urlpatterns = [
    path("jobs/", getAllJobs, name="jobs"),
]
