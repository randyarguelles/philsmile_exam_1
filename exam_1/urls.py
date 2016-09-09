from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from . import views
# from django.views.generic import TemplateView
# from django.contrib.auth.views import login
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, name='login_time'),
    url(r'^logout/$', views.logout_page),
    url(r'^register/$', views.register_page),
    url(r'^register/success/$', TemplateView.as_view(
        template_name="registration/register_success.html")),
    # Start Quiz dito
    url(r'^quiz/(?P<pk>[0-9]+)/$', views.quiz_detail,  name='quiz'),
    url(r'^results/(?P<pk>[0-9]+)$', views.results,  name='results'),


]
