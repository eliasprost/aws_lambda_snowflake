import pandas as pd
import snowflake.connector as snf
from app.src.aws import SecretManager
from app.parameters import SNOWFLAKE_USER_VARIABLE, SNOWFLAKE_PASSWORD_VARIABLE, SNOWFLAKE_ACCOUNT_VARIABLE

def get_connection_from_secret(secret_json,  secret=None):
    return SnowflakeConnection(
        user=secret_json[SNOWFLAKE_USER_VARIABLE],
        password=secret_json[SNOWFLAKE_PASSWORD_VARIABLE],
        account=secret_json[SNOWFLAKE_ACCOUNT_VARIABLE])

class SnowflakeConnection:
    def __init__(self, user, password, account):
        self.connection = snf.connect(user=user, password=password, account=account)
        self.cursor = self.connection.cursor()

    def query_to_df(self, cursor, query, params=None):
        self.cursor.execute(query)
        self.column_names = [i[0] for i in self.cursor.description]
        self.df = pd.DataFrame(self.cursor.fetchall(), columns = self.column_names)
        self.connection.close()
        self.cursor.close()
        
        return self.df
