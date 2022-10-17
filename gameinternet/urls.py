from django.urls import path, re_path
from .views import InternetView, IpView, IpConnectView, disconnectuser
app_name = "gameinternet"


urlpatterns = [
    re_path(r"^netip=(?:(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)\.){3}(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)$", IpView, name="gameinternet"),
    re_path(
        r"^netip=(?:(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)\.){3}(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)isconnected=ok$",
        IpConnectView, name="gameinternet"),
re_path(
        r"^netip=(?:(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)\.){3}(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)logout$",
        disconnectuser, name="gameinternet"),

    path('internet/', InternetView, name="gameinternet")

]

