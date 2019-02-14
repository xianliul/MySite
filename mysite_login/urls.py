from django.conf.urls import url
from django.contrib import admin
from login import views
from django.urls import re_path
from login.views import ActiveUserView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active")
]
