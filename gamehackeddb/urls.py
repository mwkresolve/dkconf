from django.urls import path
from .views import dbview

app_name = "gamehackeddb"

urlpatterns = [
    path("database/", dbview, name="gamehackeddb"),

]
