from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to
from django.utils.translation import ugettext_lazy as _
from atados.core.forms import AuthenticationForm, SearchForm
from atados.core.views import home, CityView, SuburbView
from haystack.views import SearchView

urlpatterns = patterns(
    '',

    url(r'^$', home, name='home'),

    url(_(r'^sign-in$'), 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
         'template_name': 'atados/core/sign-in.html'}, name='sign-in'),

    url(r'^sign-in$', redirect_to,
        {'url': _('/sign-in'),
         'query_string': True}, name='global-sign-in'),

    url(_(r'^sign-out$'), 'django.contrib.auth.views.logout',
        {'next_page': _('/sign-in')}, name='sign-out'),

    url(_(r'^search$'), SearchView(form_class=SearchForm), name='search'),

    url(_(r'^terms$'), direct_to_template,
        {'template': 'atados/core/terms.html'}, name='terms'),

    url(_(r'^privacy$'), direct_to_template,
        {'template': 'atados/core/privacy.html'}, name='privacy'),

    url(_(r'^security$'), direct_to_template,
        {'template': 'atados/core/security.html'}, name='security'),

    url(_(r'^about$'), direct_to_template,
        {'template': 'atados/core/about.html'}, name='about'),

    url(r'^city/(?P<state>[0-9]+)$', CityView.as_view()),
    url(r'^suburb/(?P<city>[0-9]+)$', SuburbView.as_view()),
)
