import requests

API_TOKEN = 'dWwJKu19p630TdrOuO9pbRk2tMcVseWUD8p1ZToM'
API_URL = 'https://api.marketaux.com/v1/'
BASE_API_PARAMS = {
    'api_token': API_TOKEN,
    'language': ['en'],
}
DEFAULT_DOMAINS = [
    'seekingalpha.com',
    'foxbusiness.com',
    'wsj.com',
    'money.cnn.com',
    'investopedia.com',
    'finance.yahoo.com',
    'forbes.com',
    'bloomberg.com',
    'cnbc.com',
    'cnn.com',
    'marketwatch.com',
    'nytimes.com',
    'reuters.com',
    'thestreet.com',
]

DEFAULT_SYMBOLS = [
    'TSLA',
    'GME',
    'AMC',
    'HOOD',
    'COIN',
    'NIO',
    'RIVN',
    'AAPL',
    'COIN',
]


def get_endpoint(endpoint: str, **extra_params):
    endpoint_url = API_URL + endpoint
    request_params = {
        **BASE_API_PARAMS,
        **extra_params,
    }

    # Stringify parameters with a list as a value
    for name, value in request_params.items():
        if type(value) == list:
            request_params[name] = ','.join(value)

    response = requests.get(endpoint_url, params=request_params)
    return response.json()


def get_all_pages(get_page):
    result_data = []
    page_number = 1
    pages_left = True
    while pages_left:
        page_response = get_page(page=page_number)

        page_data = page_response['data']
        if page_data:
            result_data += page_data

        page_meta = page_response['meta']
        found = page_meta['found']
        limit = page_meta['limit']
        pages_left = page_number * limit < found

        page_number += 1

    return result_data


def get_market_news(symbols=None, page=1):
    news_results = get_endpoint(
        'news/all',
        domains=DEFAULT_DOMAINS,
        page=page,
        symbols=symbols if symbols else DEFAULT_SYMBOLS
    )

    # Filter the matching entities for each article if a list of symbols is provided
    if symbols:
        symbol_lookup = set(symbols)
        for article in news_results['data']:
            article['entities'] = list(filter(
                lambda entity: entity['symbol'] in symbol_lookup,
                article['entities']
            ))

    return news_results


def search_entities(search_value: str):
    return get_endpoint('entity/search', search=search_value)


def get_sources(page=1):
    endpoint_url = API_URL + 'news/sources'
    response = requests.get(endpoint_url, params={**BASE_API_PARAMS, 'page': page})
    return response.json()

