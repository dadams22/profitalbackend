import requests

API_TOKEN = 'dWwJKu19p630TdrOuO9pbRk2tMcVseWUD8p1ZToM'
API_URL = 'https://api.marketaux.com/v1/'
BASE_API_PARAMS = {
    'api_token': API_TOKEN,
    'language': ['en'],
}
DEFAULT_DOMAINS = [
    # 'seekingalpha.com',
    # 'foxbusiness.com',
    # 'wsj.com',
    # 'money.cnn.com',
    # 'investopedia.com',
    # 'finance.yahoo.com',
    # 'forbes.com',
    # 'bloomberg.com',
    # 'cnbc.com',
    # 'cnn.com',
    'marketwatch.com',
    # 'nytimes.com',
    # 'reuters.com',
    # 'thestreet.com',
]

DEFAULT_SYMBOLS = [
    # 'TSLA',
    # 'GME',
    # 'AMC',
    # 'HOOD',
    # 'COIN',
    # 'NIO',
    # 'RIVN',
    'AAPL',
    # 'COIN',
]


def get_endpoint(endpoint: str, **EXTRA_PARAMS):
    endpoint_url = API_URL + endpoint
    request_params = {
        **BASE_API_PARAMS,
        **EXTRA_PARAMS,
    }
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
        print(page_number, found, limit, pages_left)

        page_number += 1

    return result_data


def get_market_news(symbols=None, page=1):
    return get_endpoint(
        'news/all',
        domains=DEFAULT_DOMAINS,
        page=page,
        symbols=DEFAULT_SYMBOLS
    )


def get_sources(page=1):
    endpoint_url = API_URL + 'news/sources'
    response = requests.get(endpoint_url, params={**BASE_API_PARAMS, 'page': page})
    return response.json()

