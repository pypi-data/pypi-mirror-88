from webutils.baseacct.config import Config
from webutils.baseacct import views

from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


config = Config()

urlpatterns = [
    url(r'^login/$',
        auth_views.LoginView.as_view(
            template_name='baseacct/login.html',
            authentication_form=config.get_login_form(),
        ), name='baseacct-login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(
            template_name='baseacct/logout.html',
        ), name='baseacct-logout'),
    url(r'^logout-login/$',
        auth_views.logout_then_login,
        {'login_url': config.get_login_url()},
        name='baseacct-logout-login'),
    url(r'^password_change/$',
        views.password_change, {
            'template': 'baseacct/password_change.html',
            'password_change_redirect': config.get_password_change_redirect(),
            'password_change_form': config.get_password_change_form(),
        }, name='baseacct-password-change'),
    url(r'^password_change/done/$',
        TemplateView.as_view(
            template_name='baseacct/password_change_done.html'
        ), name='baseacct-password-change-done'),
    url(r'^reset/$',
        views.reset, {
            'template': 'baseacct/reset.html',
            'reset_form': config.get_reset_form(),
            'profile_model': config.get_profile_model(),
        }, name='baseacct-reset'),
    url(r'^reset/(?P<key>\w+)/$',
        views.reset, {
            'template': 'baseacct/reset_complete.html',
            'reset_form': config.get_reset_form(),
            'profile_model': config.get_profile_model(),
        }, name='baseacct-reset-key'),
]
