import json
import boto3 as boto3
from botocore.exceptions import ClientError
from app.src.exceptions import SecretNotFoundException

class SecretManager:
    def __init__(self, key):
        self._key = key

    def _secret_value(self):
        try:

            session = boto3.session.Session()
            client = session.client(service_name="secretsmanager")
            secret = client.get_secret_value(SecretId=self._key)

            if "SecretString" in secret:
                return secret["SecretString"]

        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise SecretNotFoundException()

    def get_value(self):
        secret = self._secret_value()

        if secret:
            return json.loads(secret)

        raise SecretNotFoundException()
