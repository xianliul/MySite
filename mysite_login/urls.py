from django.conf.urls import url
from django.contrib import admin
from login import views
from django.urls import re_path, path
from login.views import ActiveUserView, ForgetPwdView, ResetView, ModifyView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<str:active_code>', ResetView.as_view(), name='reset'),
    path('modify/', ModifyView.as_view(), name='modify'),
]
