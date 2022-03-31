import requests
import json

from news.marketaux_api import get_sources, get_all_pages

DATA_FILEPATH = 'script_data/source_list.json'


def get_source_list():
    source_list = get_all_pages(get_sources)
    print(len(source_list))

    with open(DATA_FILEPATH, 'w') as data_file:
        json.dump(source_list, data_file)

    return source_list


if __name__ == '__main__':
    print(get_source_list())
