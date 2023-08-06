"""
pygiftbit
Copyright 2020 Donald Brown
https://github.com/donaldkbrown/pygiftbit
OSI Compliant: MIT License

A simple API wrapper for the Giftbit Gift API.
"""

from time import sleep
from requests import get, post, delete, put
from pygiftbit.errors import AuthError, APIError, CampaignError, ConflictError, FundError, GiftError, KeyLengthError, RegionError
from os import environ
from urllib.parse import urlencode
from datetime import datetime
from json import dumps
from logging import warning

TESTBED_HOST = 'https://api-testbed.giftbit.com/papi/v1'
PRODUCTION_HOST = 'https://api.giftbit.com/papi/v1'


def check_args(subject, message, gift_template):
    """
    This will raise an error if an improper
    combination of arguments is passed.
    """
    if gift_template and (subject or message):
        raise ConflictError('Supply only gift_template OR subject and message.')
    elif not gift_template and not (subject and message):
        raise ConflictError('You must supply both subject and message if not supplying template.')


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

        api_key = api_key or environ.get('GIFTBIT_API_KEY', '')

        if len(api_key) != 258:
            raise KeyLengthError(len(api_key))

        self.headers = {
            'Authorization': 'Bearer ' + api_key,
            'Accept-Encoding': 'identity',
            'Content-Type': 'application/json'
        }
        ping_check = get(
            self.host + '/ping',
            headers=self.headers
        )
        if ping_check.status_code in [401, 403]:
            raise AuthError(ping_check.status_code)
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

    def create_campaign(
        self,
        expiration_date: str,
        contacts: list,
        brand_codes: list,
        price_in_cents: int,
        id: str,
        message='',
        subject='',
        gift_template='',
    ):
        """
        Create a new campaign to send a choose-your-own
        gift card to multiple users at once. All arguments
        are required, with some constraints:

        gift_template is required only if message and subject
        are omitted. It is ignored if message or subject is set.
        message and subject must both be set. If only one is
        set, an error will be raised.

        expiration_date: A date string in YYYY-MM-dd format. After 11:59:59 PM PST
          on this date, the campaign will end.
        contacts: A list of dict objects containing keys email, firstname, and lastname.
          If any key is not supplied in any dict, the whole request will fail.
        brand_codes: A list of brand codes for the users to choose from. Use Client.get_brand_codes()
        price_in_cents: An integer number of the value for the gift-card.
        id: A memorable name for this campaign, must be unique.
        message: The gift-card message. Not to be used with a template.
        subject: The subject of the email to send. Not to be used with a template.
        gift_template: The name of the email template you have created on the Giftbit website.
        """
        check_args(subject, message, gift_template)
        if len(contacts) < 1:
            raise ConflictError('You must supply at least one contact.')
        expected_keys = ['email', 'firstname', 'lastname']
        for contact in contacts:
            if not (
                all(
                    key in expected_keys for key in contact
                ) and all(
                    key in contact for key in expected_keys
                )
            ):
                raise ConflictError("Contacts must be dicts containing email, lastname, and firstname.")
        parsed_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        if parsed_date <= datetime.today():
            raise ConflictError('Expiration date must be in the future!')
        if len(brand_codes) < 1:
            raise ConflictError('You must supply at least one brand code!')
        payload = {
            'brand_codes': brand_codes,
            'price_in_cents': price_in_cents,
            'contacts': contacts,
            'expiry': expiration_date,
            'id': id
        }
        if gift_template:
            payload['gift_template'] = gift_template
        else:
            payload['subject'] = subject
            payload['message'] = message
        attempts = 0
        while attempts < 3:
            campaign_response = post(
                self.host + '/campaign',
                headers=self.headers,
                data=dumps(payload)
            )
            if campaign_response.status_code == 200:
                campaign_info = campaign_response.json()['campaign']
                results = {
                    'server_uuid': campaign_info['uuid'],
                    'user_created_id': campaign_info['id'],
                    'status': campaign_info['status'],
                    'sent_to': campaign_info['contacts']
                }
                return results
            elif campaign_response.status_code == 429:
                attempts += 1
                warning(f"Request timed out, trying again {3 - attempts} more time(s).")
                sleep(1.5)
            else:
                error_message = campaign_response.json()['error']['message']
                error_name = campaign_response.json()['error']['name']
                raise CampaignError(f'{error_name}: {error_message}')
        raise CampaignError('Rate Limited: Rate limited the request three times in a row and could not complete.')

    def check_campaign(self, campaign_id: str):
        """
        Get the status of a previously created campaign.

        campaign_id must be a valid campaign ID created by
        the user in a previous Client.create_campaign() request.
        """
        campaign_request = get(
            self.host + f'/campaign/{campaign_id}',
            headers=self.headers
        )
        if campaign_request.status_code != 200:
            error_name = campaign_request.json()['error']['name']
            error_message = campaign_request.json()['error']['message']
            raise CampaignError(f'{error_name}: {error_message}')
        data = campaign_request.json()['campaign']
        return data

    def check_funds(self):
        """
        Check your current funding balances.
        """
        fund_request = get(
            self.host + '/funds',
            headers=self.headers
        )
        data = fund_request.json()['fundsbycurrency']
        return data

    def add_funds(self, currency: str, amount_in_cents: int):
        """
        Add funds of the desired currency using the credit
        card on file for your account.
        """
        if currency not in ['USD', 'CAD']:
            raise FundError('Currency must be "USD" or "CAD".')
        if not isinstance(amount_in_cents, int):
            raise FundError('amount_in_cents must be an int')
        if amount_in_cents < 25000:
            raise FundError('You must fund at lest 25000 cents')
        if amount_in_cents > 1000000:
            raise FundError('You cannot fund more than 1000000 cents.')
        fund_request = post(
            self.host + '/funds',
            headers=self.headers,
            data=dumps({
                'currencyisocode': currency,
                'fund_amount_in_cents': amount_in_cents,
                'id': f'pygiftbit_fund_add_{datetime.now().isoformat().replace(" ", "_")}'
            })
        )
        if fund_request.status_code != 200:
            error_name = fund_request.json()['error']['name']
            error_message = fund_request.json()['error']['message']
            raise FundError(f'{error_name}: {error_message}')
        data = fund_request.json()['fundsbycurrency']
        return data

    def list_gifts(self, **filters):
        """
        List previously sent gifts and their statuses,
        searching with filters. Some default filters
        are pre-set:

        limit: 20 - how many results to return
        offset: 0 - offset search by this number, used with limit
        sort: delivery_status - What to sort by. Options are:
            campaign_id
            price_in_cents
            recipient_name
            recipient_email
            delivery_status
            status
        order: desc - How to order the sort, can be asc or desc

        Additional filters are available in the Giftbit API docs:
            https://www.giftbit.com/giftbitapi/#/reference/1/gifts/list-gifts
        """

        search_filters = {
            'limit': 20,
            'offset': 0,
            'sort': 'delivery_status',
            'order': 'desc'
        }
        search_filters.update(filters)
        filter_string = urlencode(search_filters)
        search_request = get(
            self.host + '/gifts?' + filter_string,
            headers=self.headers
        )
        if search_request.status_code != 200:
            error_name = search_request.json()['error']['name']
            error_message = search_request.json()['error']['message']
            raise GiftError(f'{error_name}: {error_message}')
        data = search_request.json()['gifts']
        return data

    def get_gift_status(self, uuid: str):
        """
        Get information and status of a previously sent
        gift. The uuid must be from a previously created gift,
        returned with Client().list_gifts()
        """
        gift_request = get(
            self.host + f'/gifts/{uuid}',
            headers=self.headers
        )
        if gift_request.status_code != 200:
            error_name = gift_request.json()['error']['name']
            error_message = gift_request.json()['error']['message']
            raise GiftError(f'{error_name}: {error_message}')
        data = gift_request.json()['gift']
        return data

    def cancel_gift(self, uuid):
        """
        Cancel a gift that was previously sent
        out. The uuid can be found with Client().list_gifts()
        """
        gift_request = delete(
            self.host + f'/gifts/{uuid}',
            headers=self.headers
        )
        if gift_request.status_code != 200:
            error_name = gift_request.json()['error']['name']
            error_message = gift_request.json()['error']['message']
            raise GiftError(f'{error_name}: {error_message}')
        data = gift_request.json()['gift']
        return data

    def resend_gift(self, uuid):
        """
        Resend an email for a gift that was previously sent
        out. The uuid can be found with Client().list_gifts().
        This is used if a gift is in the TEMPORARILY_UNDELIVERABLE
        state and needs resent.
        """
        gift_request = put(
            self.host + f'/gifts/{uuid}',
            headers=self.headers
        )
        if gift_request.status_code != 200:
            error_name = gift_request.json()['error']['name']
            error_message = gift_request.json()['error']['message']
            raise GiftError(f'{error_name}: {error_message}')
        data = gift_request.json()['gift']
        return data

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
