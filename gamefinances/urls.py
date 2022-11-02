from django.urls import path
from .views import FinancesView


app_name = "gamefinances"


urlpatterns = [
    path("finances/", FinancesView.as_view(), name="gamefinances"),

]
