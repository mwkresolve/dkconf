from django.urls import path
from .views import Controller
from django.contrib.auth.decorators import login_required

app_name = "controller"

urlpatterns = [
    path("controller", Controller.as_view(), name="controller"),

]
