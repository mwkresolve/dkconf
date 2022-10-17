from django.urls import path
from .views import SoftwareView

app_name = "gamesoftware"

urlpatterns = [
    path("software/", SoftwareView.as_view(), name="gamesoftware"),

]
