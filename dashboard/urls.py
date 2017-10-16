from dashboard import views
from django.conf.urls import url


urlpatterns = [
    url(r'^sign-up/$', views.sign_up, name="sign-up"),
    url(r'^sign-in/$', views.get_token, name="get_token"),
    url(r'^sign-in/token/$', views.sign_in, name="sign-in"),
    url(r'^user/$', views.dashboard_view, name="dashboard-view"),
]
