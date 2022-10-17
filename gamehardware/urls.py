from django.urls import path
from .views import HardwareView

app_name = "gamehardware"

urlpatterns = [
    path("hardware/", HardwareView.as_view(), name="gamehardware"),

]
