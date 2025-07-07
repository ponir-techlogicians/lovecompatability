from django.urls import path

from django.contrib.auth import views as auth_views


from app.api_views import CalculateAPIView, ResultDetailAPIView, SaveLocationAPIView, CreatePaymentIntentAPIView, \
    ListAPIView, SearchAPIView, SubscriptionValidationView, RestorPurchaseView, GooglePlayBillingNotification, \
    IosBillingNotification, UsageLeftView, LanguageListAPIView
from app.views import DashboardView, SearchBasicView, set_language_view, CalculateView, SearchView, ListView, \
    save_location, ResultDetailView, create_checkout_session, auto_suggest_names

urlpatterns = [
    path('set_language/', set_language_view, name='set_language'),
    path('suggest-name/', auto_suggest_names, name='suggest-name'),

    # path('calculate/', CalculateView.as_view(), name='calculate'),
    path("result/<int:id>/", ResultDetailView.as_view(), name="compatibility_result_detail"),
    path("save-location/", save_location, name="save_location"),
    path("search/", SearchView.as_view(), name="search"),
    path("list/", ListView.as_view(), name="list"),

    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("search-basic/", SearchBasicView.as_view(), name="search-basic"),

    path('api/calculate/', CalculateAPIView.as_view(), name='calculate-api'),
    path('api/language-list/', LanguageListAPIView.as_view(), name='language-list-api'),
    path('api/result/<int:id>/', ResultDetailAPIView.as_view(), name='result-detail-api'),

    path('api/save-location/', SaveLocationAPIView.as_view(), name='save-location-api'),

    path('api/search/', SearchAPIView.as_view(), name='search-api'),

    path('api/list/', ListAPIView.as_view(), name='list-api'),
    path('api/usage-left/', UsageLeftView.as_view(), name='usage-left-api'),

    path('api/create-payment-intent/', CreatePaymentIntentAPIView.as_view(), name='create-payment-intent'),

    path('api/validate-subscription/', SubscriptionValidationView.as_view(), name='validate_subscription'),
    path('api/restore-subscription/', RestorPurchaseView.as_view(), name='restore_subscription'),
    path('api/google-play-billing-notification/', GooglePlayBillingNotification.as_view(), name='google-play-billing-notification'),
    path('api/ios-billing-notification/', IosBillingNotification.as_view(), name='ios-billing-notification'),
]
