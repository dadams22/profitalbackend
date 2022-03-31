import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.account_subtype import AccountSubtype
from plaid.model.account_subtypes import AccountSubtypes
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser

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