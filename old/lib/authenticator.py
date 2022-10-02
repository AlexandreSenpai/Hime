import os

from google.cloud import client as Service

class Auth:
    def __init__(self, service: Service, credentials_path: str):
        self._service = service 
        self._credentials_path = credentials_path

        self._client = self._set_credentials()
        
    @property
    def client(self):
        return self._client

    def _set_credentials(self):
        if os.path.isfile(self._credentials_path):
            return self._service.from_service_account_json(self._credentials_path)