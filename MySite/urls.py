from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'^home$', view.home),
    url(r'^register$', view.register),
    url(r'^login$', view.login),
]