import requests

class OmgLolApi:
    BASE_URL = 'https://api.omg.lol'
    HEADERS = {'Authorization': 'Bearer api_key'}

    def __init__(self, api_key):
        self.HEADERS['Authorization'] = f'Bearer {api_key}'
        
    def get_user_info(self, email):
        return self._get(f'/account/{email}/info')

    def get_user_addresses(self, email):
        response = self._get(f'/account/{email}/addresses')
        if response:
            return [addr['address'] for addr in response['response']]
        return []

    def get_active_sessions(self, email):
        return self._get(f'/account/{email}/sessions')

    def get_account_settings(self, email):
        return self._get(f'/account/{email}/settings')

    def set_account_settings(self, email, settings):
        return self._post(f'/account/{email}/settings', settings)

    def _get(self, endpoint):
        try:
            response = requests.get(f'{self.BASE_URL}{endpoint}', headers=self.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
        except requests.exceptions.RequestException as err:
            print(f'Request error occurred: {err}')
        else:
            return response.json()

    def _post(self, endpoint, data):
        try:
            response = requests.post(f'{self.BASE_URL}{endpoint}', headers=self.HEADERS, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
        except requests.exceptions.RequestException as err:
            print(f'Request error occurred: {err}')
        else:
            return response.json()