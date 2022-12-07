from django.urls import path, re_path
from .views import tasks_view, complete_task

app_name = "gameusertasks"

urlpatterns = [
    path("task/", tasks_view, name="gameusertasks"),
    re_path(r"^taskcompleteid=[0-9]+$", complete_task, name="gameusertasks"),

]