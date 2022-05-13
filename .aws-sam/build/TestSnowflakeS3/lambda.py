# -*- coding: utf-8 -*-

import logging
import boto3
from datetime import datetime
import io
import pandas as pd
import snowflake.connector
import json
import os
from app.src.exceptions import SecretNotFoundException, InvalidSourceException
from app.src.aws import SecretManager
from app.src.db import get_connection_from_secret, SnowflakeConnection
from app.parameters import BUCKET_NAME, QUERY, SNOWFLAKE_CREDENTIALS_NAME
from app.utils import write_dataframe_to_s3

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def lambda_handler(event, context):
    log.info(event)
    
    # Load credential JSON from environment
    SNOWFLAKE_CRED_JSON = json.loads(os.environ.get(SNOWFLAKE_CREDENTIALS_NAME, {}))
    
    # Snowflake connection
    try:
        connection = get_connection_from_secret(secret_json = SNOWFLAKE_CRED_JSON)
    except Exception as e:
        log.info({"ERROR":"An error has ocurred when trying to make a connection with Snowflake"})
        raise(e)
    
    # Executing query
    try:
        df = connection.query_to_df(query = QUERY,
                                    cursor = connection.cursor)
        log.info({"INFO":"SQL query in Snowflake has executed successfully"})
    except Exception as e:
        log.info({"ERROR":"An error has ocurred when trying to execute the SQL query"})      
        raise(e)
    
    # Write DF to S3
    try:
        write_dataframe_to_s3(df, bucket = BUCKET_NAME)
        log.info({"INFO":"CSV to S3 has been put completed in S3 bucket"})
    except Exception as e:
        log.info({"ERROR":"An error has ocurred when trying to write the df in s3 bucket"})
        raise(e)
    return

if __name__ == '__main__':
    response = lambda_handler(None, None)
