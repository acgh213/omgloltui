import getpass
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from omglol_api import OmgLolApi  # Import the API class from the omglol_api.py file

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
    addresses_text_area = TextArea(text=f"Addresses:\n{addresses_text}@omg.lol")

        
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