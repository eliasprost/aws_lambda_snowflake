import pandas as pd
import io
import boto3
from datetime import datetime

def write_dataframe_to_s3(dataframe: pd.DataFrame,
                          bucket: str):
    with io.StringIO() as csv_buffer:
        dataframe.to_csv(csv_buffer, index = False, encoding = 'utf-8')
        s3 = boto3.resource('s3')
        session = boto3.Session()
        dev_s3_client = session.client('s3')
        response = dev_s3_client.put_object(
            Bucket=bucket,
            Key= bucket + str(datetime.today().strftime('-%Y-%m-%d-%H-%M-%S')) + '.csv',
            Body=csv_buffer.getvalue()
        )