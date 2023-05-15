import requests
import getpass
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings

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


def main():
    api_key = getpass.getpass("Enter your API key: ")
    email = input("Enter your email: ")
    api = OmgLolApi(api_key)

    # Retrieve user info
    user_info = api.get_user_info(email)
    if user_info:
        email_text_area = TextArea(text=f"Email: {user_info.get('response').get('email', '')}")
        name_text_area = TextArea(text=f"Name: {user_info.get('response').get('name', '')}")

    # Retrieve user addresses
    user_addresses = api.get_user_addresses(email)
    addresses_text = "\n".join([f"Address: {addr}" for addr in user_addresses])
    addresses_text_area = TextArea(text=f"Addresses:\n{addresses_text}")

        
    # Retrieve user sessions
    user_sessions = api.get_active_sessions(email)
    if user_sessions:
        sessions_text_area = TextArea(text=f"Active Sessions: {', '.join(user_sessions)}")
    
     # Retrieve account settings
    account_settings = api.get_account_settings(email)
    if account_settings:
        account_settings_area = TextArea(text=f"Account Settings: {account_settings}")
    kb = KeyBindings()

    @kb.add('q')
    def _(event):
        " Quit when 'q' is pressed. "
        event.app.exit()

    # Update layout with the new section for account settings
    root_container = HSplit([email_text_area, name_text_area, addresses_text_area, sessions_text_area, account_settings_area])
    layout = Layout(root_container)
    app = Application(layout=layout, full_screen=True, key_bindings=kb)
    app.run()

if __name__ == '__main__':
    main()
