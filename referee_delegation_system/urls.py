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
from django.urls import path

from referees.views import RefereesListView, RefereeDetailView
from accounts.views import ProfileRefereeAddView, ProfileRefereeEditView, ProfileRefereeDeleteView
from competitions.view_home import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('referees/referees/', RefereesListView.as_view(), name='referees_list'),
    path('referees/referee/<pk>/', RefereeDetailView.as_view(), name='referee_detail'),

    path('accounts/profilereferee/add/', ProfileRefereeAddView.as_view(), name='profile_referee_add'),
    path('accounts/profilereferee/<pk>/edit/', ProfileRefereeEditView.as_view(), name='profile_referee_edit'),
    path('accounts/profilereferee/<pk>/delete/', ProfileRefereeDeleteView.as_view(), name='profile_referee_delete'),
]
