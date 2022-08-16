import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
# from plaid.model.account_subtype import AccountSubtype
# from plaid.model.account_subtypes import AccountSubtypes
# from plaid.model.depository_filter import DepositoryFilter
# from plaid.model.link_token_account_filters import LinkTokenAccountFilters

config = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': '62005d2b80f318001a7419b5',
        'secret': '4816f4049230289acc794a887b6bc9',
    }
)

api_client = plaid.ApiClient(config)
client = plaid_api.PlaidApi(api_client)


def obtain_link_token(user_id):
    request = LinkTokenCreateRequest(
        products=[Products('investments')],
        client_name="Profital",
        country_codes=[CountryCode('US')],
        language='en',
        # webhook='https://sample-webhook-uri.com',
        link_customization_name='default',
        # account_filters=LinkTokenAccountFilters(
        #     depository=DepositoryFilter(
        #         account_subtypes=AccountSubtypes(
        #             [AccountSubtype('checking'), AccountSubtype('savings')]
        #         )
        #     )
        # )
        user=LinkTokenCreateRequestUser(
            client_user_id=str(user_id)
        )
    )

    # create link token
    response = client.link_token_create(request)
    link_token = response['link_token']

    return link_token


def exchange_public_token(public_token: str):
    # the public token is received from Plaid Link
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    return exchange_response['access_token']


def get_holdings(access_token):
    holdings_request = InvestmentsHoldingsGetRequest(access_token=access_token)
    holdings_response = client.investments_holdings_get(holdings_request)
    result = holdings_response.to_dict()

    # Clean the response to focus on the data we need in the structure we need it in
    holdings = holdings_response['holdings']
    securities = holdings_response['securities']

    securities_lookup = {security['security_id']: security for security in securities}
    holdings_with_security_info = []
    for holding in holdings:
        security_id = holding['security_id']
        security = securities_lookup[security_id]
        holdings_with_security_info.append({**security.to_dict(), **holding.to_dict()})

    investment_balance = 0
    for account in holdings_response['accounts']:
        balances = account['balances']
        investment_balance += balances['current']

    return {'balance': investment_balance, 'holdings': holdings_with_security_info}
