import requests
import getpass
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Frame, TextArea


class OmgLolApi:
    BASE_URL = 'https://api.omg.lol'
    HEADERS = {'Authorization': 'Bearer api_key'}

    def __init__(self, api_key):
        self.HEADERS['Authorization'] = f'Bearer {api_key}'

    def get_user_info(self, email):
        try:
            response = requests.get(f'{self.BASE_URL}/account/{email}/info', headers=self.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print("User not found. Please check your email address.")
            else:
                print("An error occurred while fetching the user information.")
        except requests.exceptions.RequestException as err:
            print("Unable to connect to the server. Please check your internet connection and try again.")
        except ValueError:
            print("Received unexpected response from the server. Please try again later.")
        return None

def main():
    api_key = getpass.getpass("Enter your API key: ")
    email = input("Enter your email: ")
    api = OmgLolApi(api_key)
    user_info = api.get_user_info(email)
    if user_info:
        email_text_area = TextArea(text=f"Email: {user_info.get('response').get('email', '')}")
        name_text_area = TextArea(text=f"Name: {user_info.get('response').get('name', '')}")
        root_container = HSplit([email_text_area, name_text_area])
        layout = Layout(root_container)
        app = Application(layout=layout, full_screen=True)
        app.run()

if __name__ == '__main__':
    main()
