from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import webbrowser
from pathlib import Path
from cleverdict import CleverDict
import pyperclip
import inspect
import json
import keyring
from .clevergui import start_gui, button_menu, text_input
from .cleverutils import to_json, timer
from .cleverwebutils import Login_to
import threading

class CleverSession(CleverDict):
    """
    A CleverDict sub-class(*) intended to handle selenium webbrowser sessions
    and common repeatable tasks such as selecting a target website using
    PySimpleGUI, retrieving login credentials using keyring, automated login,
    and scraper/collection tasks.

    Also uses predefined login and scraper functions notably from:

    login_to.py
    collect.py

    (*) CleverDict provides easy data handling and auto-save features.
    """
    index = CleverDict()
    choices = {"https://github.com/login": "Github",
               "https://twitter.com": "Twitter",
               "https://www.satchelone.com/login": "SatchelOne"}
    keyring_config_root = keyring.util.platform_.config_root()
    keyring_data_root = keyring.util.platform_.data_root()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        start_gui()
        self.check_and_prompt("url")
        if self.get("url"):
            self.account = CleverSession.choices[self.url]
            self.get_username()
        if not self.get("dirpath"):
            self.dirpath = Path().cwd()

    def get_username(self):
        """
        Loads (last modified) username from keyring. May not work on iOS.
        """
        try:
            self.username = keyring.get_credential(self.account, None).username
        except:
            print("\n  ⚠ .get_username() only supported on Windows OS.")
            print("\n     Trying creating .username manually first.")

    def check_and_prompt(self, *args):
        """
        Checks for existence/non-False value of an argument, and if required
        calls the specified method to prompt for a value.  Different methods
        may be needed for different input types e.g. file, folder, checkboxes, database read, REST API call, or regular input().

        args : attributes (as strings) to look for; try to use logical order.
        """
        buttons = {"url": "Please enter a link (URL) to the target website:",}
        text = {"username": "Please enter a username/login ID{}:",
                "password": "Please enter a password{}:"}
        choices = CleverSession.choices
        for attribute in args:
            prompt = buttons.get(attribute) or text.get(attribute) or f"Please enter a value for .{attribute} :"
            prompt = prompt.replace("{}", f" for your {self.account} account" if self.get("account") else "")
            if attribute == "password":
                self.check_and_prompt("url", "username")
                if not keyring.get_password(choices[self.url], self.username):
                    self.set_password(text_input(prompt))
            elif not self.get(attribute):
                if attribute in buttons:
                    value = button_menu(choices)
                else:  # Includes attributes in neither buttons nor text
                    value = text_input(prompt)
                if value:
                    self[attribute] = value

    @property
    def password(self):
        """ Retrieve password from keyring """
        return keyring.get_password(CleverSession.choices[self.url], self.username)

    def set_password(self, value):
        """ Set password in keyring """
        if value:
            keyring.set_password(CleverSession.choices[self.url], self.username, value)

    def delete_password(self):
        """
        Delete password AND username from keyring.
        .username remains in memory but .password was only ever an @property.
        """
        keyring.delete_password(CleverSession.choices[self.url], self.username)

    @timer
    def login_with_webbrowsers(self, **kwargs):
        """
        KWARGS:

        wait : Seconds for selenium to implicitly_wait
        browsers : int > number of browsers to run concurrently
        """
        self.check_and_prompt("url", "username", "password")
        if not hasattr(self, "browsers"):
            self.browsers = []
        for n in range(kwargs.get("browsers") or 1):
            self.browsers += [webdriver.Chrome()]
        dispatch = {"github.com": Login_to.github,
                    "twitter.com": Login_to.twitter,
                    "satchelone.com": Login_to.satchelone}
        browserThreads = []
        for browser in self.browsers:
            browser.implicitly_wait(kwargs.get("wait") or 3)
            for website, func in dispatch.items():
                if website in self.url:
                    browserThread = threading.Thread(target=func, args=[self, browser])
                    browserThreads.append(browserThread)
                    browserThread.start()
                    break
        for browserThread in browserThreads:
                browserThread.join()
        self.browser = self.browsers[0]


    def save(self, name, value):
        """ Generic auto-save confirmation applied CleverDict """
        if "password" not in str(name).lower():
            print(f" ⓘ  {name} = {value} {type(value)}")

    def start(self):
        """ Shortcut/Alias for starting a webbrowser session and logging in """
        self.login_with_webbrowser()

# self= CleverSession()
# self.start()
