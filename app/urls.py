from django.urls import path

from django.contrib.auth import views as auth_views

from app.views import DashboardView, SearchBasicView, set_language_view, CalculateView, SearchView, ListView, \
    save_location, ResultDetailView, create_checkout_session

urlpatterns = [
    path('set_language/', set_language_view, name='set_language'),
    path('calculate/', CalculateView.as_view(), name='calculate'),
    path("result/<int:id>/", ResultDetailView.as_view(), name="compatibility_result_detail"),
    path("save-location/", save_location, name="save_location"),
    path("search/", SearchView.as_view(), name="search"),
    path("list/", ListView.as_view(), name="list"),

    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("search-basic/", SearchBasicView.as_view(), name="search-basic"),
]
