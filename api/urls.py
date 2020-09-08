from django.conf.urls import url
from django.contrib import admin
from .views import ChatterBotApiView

urlpatterns = [
    # url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]