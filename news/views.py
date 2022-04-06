from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status

from .marketaux_api import get_market_news
from .plaid_api import obtain_link_token, exchange_public_token, get_holdings
from .models import User
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        parent_response = super(CreateUserView, self).create(request, *args, **kwargs)

        if parent_response.status_code != 201:
            return parent_response

        username = parent_response.data.get('username')
        user = User.objects.get(username=username)

        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)



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
        user_id = self.request.user.id
        token = obtain_link_token(user_id)
        return Response({'link_token': token})


class PlaidTokenExchangeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        public_token = request.data.get('public_token')
        access_token = exchange_public_token(public_token)
        self.request.user.set_plaid_access_token(access_token)
        return Response()


class PlaidHoldingsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        access_token = user.plaid_access_token
        holdings = get_holdings(access_token)
        print(holdings)
        return Response(holdings)
