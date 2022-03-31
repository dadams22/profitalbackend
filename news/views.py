from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .marketaux_api import get_market_news
from .plaid_api import obtain_link_token


class MarketNewsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        page = request.GET.get('page', 1)
        return Response(get_market_news(page=page))


class PlaidTokenView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(self.request.user)
        user_id = self.request.user.id
        print('user id', user_id)
        token = obtain_link_token(user_id)
        print(token)
        return Response({ 'link_token': token })
