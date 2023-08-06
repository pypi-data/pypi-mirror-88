"""
pygiftbit
Copyright 2020 Donald Brown
https://github.com/donaldkbrown/pygiftbit
OSI Compliant: MIT License

A simple API wrapper for the Giftbit Gift API.
"""

from requests import get
from pygiftbit.errors import AuthError, APIError, RegionError
from os import environ
from urllib.parse import urlencode

TESTBED_HOST = 'https://api-testbed.giftbit.com/papi/v1'
PRODUCTION_HOST = 'https://api.giftbit.com/papi/v1'


class Client():
    """
    Giftbit API Client
    This is the base class that allows you
    to perform actions on the GiftBit API.
    """

    def __init__(self, api_key='', testing=True):
        """
        Initialize the client. Return an error if
        the initial ping doesn't work.

        api_key: A 258-character string. Defaults to the GIFTBIT_API_KEY environment variable.
        testing: Whether or not to use the Giftbit testbed. Defaults to true.
        """
        if testing:
            self.host = TESTBED_HOST
        else:
            self.host = PRODUCTION_HOST

        self.api_key = api_key or environ.get('GIFTBIT_API_KEY', '')

        assert len(self.api_key) == 258, "Your API key should be 258 characters."

        self.headers = {
            'Authorization': 'Bearer ' + self.api_key,
            'Accept-Encoding': 'identity',
            'Content-Type': 'application/json'
        }
        ping_check = get(
            self.host + '/ping',
            headers=self.headers
        )
        if ping_check.status_code in [401, 403]:
            raise AuthError(ping_check.status_code)
        else:
            attributes = ping_check.json()
            self.user_name = attributes['username']
            self.display_name = attributes['displayname']
        self.regions = self.list_regions()

    def list_regions(self):
        "Return a list of valid regions."
        req = get(
            self.host + '/regions',
            headers=self.headers
        )
        result = req.json()
        if req.status_code != 200:
            error_message = result['error']['code'] + ' - ' + result['error']['message']
            raise APIError(message=error_message, status_code=req.status_code)
        region_list = result['regions']
        regions = {}
        for region in region_list:
            regions[region['id']] = region['name']
        return regions

    def brand_info(self, brand_code: str):
        """
        Return information about a single
        brand of gift card.

        brand_code: A lowercase string representing a brand
        """
        brand_info = get(
            self.host + f'/brands/{brand_code}',
            headers=self.headers
        )
        print(brand_info.json())

    def get_brand_codes(self, **search_arg_modifiers):
        """
        Return a list of available brands in groups of 20.

        By providing kwargs (search_arg_modifiers) you can
        modify your search with the following parameters:

        limit - How many brands to display
        offset - How many brands to offset your limit by
        search - A search term to look for in name or description
        region - A valid region code from Client.list_regions()
        min_price_in_cents - Search only for giftcards with this minimum balance
        max_price_in_cents - Search only for giftcards with this maximum balance
        currencyisocode - Search only for giftcards in "USD", "CAD", or "AUD"
        """
        search_args = {
            'limit': 20,
            'region': 3,
            'offset': 0
        }
        search_args.update(search_arg_modifiers)
        if search_args['region'] not in self.regions:
            raise RegionError(search_args['region'])
        url_string = '/brands?' + urlencode(search_args)
        brand_list = get(
            self.host + url_string,
            headers=self.headers
        ).json()['brands']
        brands = []
        for brand in brand_list:
            brands.append(brand['brand_code'])
        return brands

    def __str__(self):
        """
        Display a string representation of the
        object as it is currently configured.
        """
        return f'Authenticated as {self.display_name} ({self.user_name}).'

    def __repr__(self):
        """
        Return a description of the client.
        """
        return f'GiftBit API Client: {self.__str__()}'
