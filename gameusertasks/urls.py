from django.urls import path, re_path
from .views import TasksView, CompleteTask

app_name = "gameusertasks"

urlpatterns = [
    path("task/", TasksView, name="gameusertasks"),
    re_path(r"^taskcompleteid=[0-9]+$", CompleteTask, name="gameusertasks"),

]