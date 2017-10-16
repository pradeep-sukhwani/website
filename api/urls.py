from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import SignUp, GetToken, SignIn, LogOut, Dashboard

urlpatterns = format_suffix_patterns([
    url(r'^register/$', SignUp.as_view(), name='register'),
    url(r'^login/$', GetToken.as_view(), name='token'),
    url(r'^login/token/$', SignIn.as_view(), name='login'),
    url(r'^login/token/$', Dashboard.as_view(), name='dashboard'),
    url(r'^logout$', LogOut.as_view(), name='log-out'),
])
