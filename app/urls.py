from django.urls import path

from django.contrib.auth import views as auth_views

from app.views import DashboardView, SearchBasicView, set_language_view, CalculateView, SearchView, ListView

urlpatterns = [
    path('set_language/', set_language_view, name='set_language'),
    path('calculate/', CalculateView.as_view(), name='calculate'),
    path("search/", SearchView.as_view(), name="search"),
    path("list/", ListView.as_view(), name="list"),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("search-basic/", SearchBasicView.as_view(), name="search-basic"),
]
