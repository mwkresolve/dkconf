from django.urls import path
from .views import financesview


app_name = "gamefinances"


urlpatterns = [
    path("finances/", financesview, name="gamefinances"),

]
