import configparser
import requests
from typing import List
import os

class ConfigFile:
    def __init__(self, path):
        self.path = path
        self.config = None
        self._load()

    def _load(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        if 'default' not in self.config:
            raise Exception(f'Error loading file {self.path} use auth to generate')

    @property
    def token(self):
        return self.config['default']['token']

    @staticmethod
    def generate(path: str, token: str):
        config = configparser.ConfigParser()
        config.add_section('default')
        config['default']['token'] = token

        with open(path, 'w') as configfile:
            config.write(configfile)


class App:
    def __init__(self, path, **kwargs):
        self.config = ConfigFile(path)
        self.endpoint = kwargs.get('endpoint', 'shopcloud-secrethub.ey.r.appspot.com')

    def read(self, secretname) -> List:
        response = requests.get(
            f'https://{self.endpoint}/hub/api/secrets',
            headers={
                'Authorization': self.config.token,
                'User-Agent': 'secrethub-cli',
            },
            params={
                'q': secretname,
            }
        )

        if not (200 <= response.status_code <= 299):
            raise Exception('API wrong answer')

        return response.json().get('results', [])

    def write(self, secretname, value):
        response = requests.post(
            f'https://{self.endpoint}/hub/api/secrets/write/',
            headers={
                'Authorization': self.config.token,
                'User-Agent': 'secrethub-cli',
            },
            json={
                'name': secretname,
                'value': value
            }
        )
        return response.json()


class SecretHub:
    def __init__(self):
        path = os.path.expanduser('~/.secrethub')
        self.app = App(path)
        self.secrets = {}

    def read(self, secretname: str):
        secret = self.secrets.get(secretname)
        if secret is not None:
            return secret.get('value')
        
        secrets = self.app.read(secretname)
        if len(secrets) == 0:
            return None
        secret = secrets[0]
        self.secrets[secret.get('name')] = secret
        return secrets[0].get('value')
