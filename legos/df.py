from Legobot.Lego import Lego
import logging
import json
import requests

logger = logging.getLogger(__name__)


class Df(Lego):
    def __init__(self, baseplate, lock):
        super().__init__(baseplate, lock)
        self.api_key = '' #put your api key here
        self.base_url = '' #put your base url here

    def listening_for(self, message):
        if message['text'] is not None:
            try:
                return message['text'].split()[0] == '!df'
            except Exception as e:
                logger.error(
                    'DF lego failed to check message text: {0!s}'.format(e))
                return False

    def handle(self, message):
        logger.info('Handling Message...')
        logger.info(message)
        opts = self._handle_opts(message)
        return_val = self._parse_args(message)
        self.reply(message, return_val, opts)

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            opts = None
            logger.error('''Could not identify message source in message:
                        {}'''.format(str(message)))
        return opts

    def _parse_args(self, message):
        return_val = 'You triggered the DF Lego!'
        parsed_message = message['text'].split()
        if len(parsed_message) < 3:
            return_val = 'You must supply at least a method and a resource path.'
        else:
            methods = ['get', 'post', 'put', 'patch', 'delete']
            method = parsed_message[1].lower()
            if method not in methods:
                return_val = method + ' not a valid method.'
            else:
                if len(parsed_message) > 3:
                    payload = self._get_payload(parsed_message)
                else:
                    payload = ''
                headers = {}
                headers['X-DreamFactory-API-Key'] = self.api_key
                request_url = self.base_url + parsed_message[2]
                if method == 'get':
                    return_val = self._make_api_call(request_url, headers, payload)
        return return_val

    def _get_payload(self, parsed_message):
        n = 3
        length = len(parsed_message)
        payload = ''
        while n < length:
            payload = payload + parsed_message[n] + ' '
            n += 1
        return payload

    def _make_api_call(self, request_url, headers, payload):
        this_request = requests.get(request_url, headers=headers)
        return this_request.text

    def get_name(self):
        return 'df'

    def get_help(self):
        return '''Call your df instance Usage: !df {method} {resource path} [payload]'''
