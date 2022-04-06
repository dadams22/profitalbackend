from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import CreateUserView, MarketNewsView, PlaidTokenView, PlaidTokenExchangeView, PlaidHoldingsView

urlpatterns = [
    path('token-auth/', obtain_auth_token),
    path('create-user/', CreateUserView.as_view()),
    path('news/', MarketNewsView.as_view()),
    path('plaid-link-token/', PlaidTokenView.as_view()),
    path('plaid-exchange-public-token/', PlaidTokenExchangeView.as_view()),
    path('holdings/', PlaidHoldingsView.as_view()),
]
