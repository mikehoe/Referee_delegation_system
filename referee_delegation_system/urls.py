"""
URL configuration for referee_delegation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.forms import user_logout
from competitions.views import MatchesListView, TeamDetailView, TeamsListView, CityAddView, CityUpdateView, \
    CitiesListView, CityDeleteView
from referees.views import RefereesListView, RefereeDetailView
from accounts.views import ProfileRefereeAddView, ProfileRefereeEditView, ProfileRefereeDeleteView
from competitions.view_home import competitions_in_season

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', competitions_in_season, name='competitions_in_season'),

    path('competitions/competitioninseason/<pk>/matches_list/', MatchesListView.as_view(), name='competition_matches'),

    path('competitions/team/<pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('competitions/teams/', TeamsListView.as_view(), name='teams_list'),
    path('competitions/cities/', CitiesListView.as_view(), name='cities_list'),
    path('competitions/city/add/', CityAddView.as_view(), name='city_add'),
    path('competitions/city/<pk>/update/', CityUpdateView.as_view(), name='city_update'),
    path('competitions/city/<pk>/delete/', CityDeleteView.as_view(), name='city_delete'),

    path('referees/referees/', RefereesListView.as_view(), name='referees_list'),
    path('referees/referee/<pk>/', RefereeDetailView.as_view(), name='referee_detail'),

    path('accounts/profilereferee/add/', ProfileRefereeAddView.as_view(), name='profile_referee_add'),
    path('accounts/profilereferee/<pk>/edit/', ProfileRefereeEditView.as_view(), name='profile_referee_edit'),
    path('accounts/profilereferee/<pk>/delete/', ProfileRefereeDeleteView.as_view(), name='profile_referee_delete'),

    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
