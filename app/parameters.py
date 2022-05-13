BUCKET_NAME = 'test-lambda-snowflake-bucket'
SNOWFLAKE_CREDENTIALS_NAME = 'SNOWFLAKE_CREDENTIALS'
SNOWFLAKE_USER_VARIABLE = 'SNOWFLAKE_USER'
SNOWFLAKE_PASSWORD_VARIABLE = 'SNOWFLAKE_PASSWORD'
SNOWFLAKE_ACCOUNT_VARIABLE = 'SNOWFLAKE_ACCOUNT'
QUERY = """
        select 
            *
        from analytics.staging.stg_production__utalk_cs_events_ack
        limit 10
        """