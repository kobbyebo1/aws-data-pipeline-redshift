import boto3
import pandas as pd
import awswrangler as wr
from datetime import date
import re
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        s3_file = event["Records"][0]["s3"]["object"]["key"]
        obj = s3_client.get_object(Bucket=bucket, Key=s3_file)

        # read csv file into dataframe using pandas
        df = pd.read_csv(obj['Body'])

        put_date = f'{date.today().strftime("%Y%m%d")}'
        dest_bucket = "our-data-lake-dev"
        dest_key = f"ingest-date={put_date}/"
        pattern = re.compile(r"[^/]*(?=.csv)")
        src_filename = "".join(pattern.findall(s3_file))
        full_dest_path = f"s3://{dest_bucket}/{dest_key}{src_filename}.parquet"


        # check if destination key exists
        def key_exists(s3_client, bucket, key):
            try:
                s3_client.head_object(Bucket=bucket, Key=key)
            except ClientError as e:
                return int(e.response['Error']['Code']) != 404
            return True

        # create key if it does not exist
        def new_key(bucket, key):
            s3_client.put_object(
                Bucket=bucket,
                Key=key
            )
            # return None

        # convert dataframe to parquet and store in datalake
        def csv_parquet(dataframe, destination):
            wr.s3.to_parquet(
                df=dataframe,
                path=destination,
                compression="snappy"
            )
            # return None

        # write parquet file, If key does not exist create one
        if key_exists(s3_client, dest_bucket, dest_key):
            csv_parquet(df, full_dest_path)
        else:
            new_key(dest_bucket, dest_key)
            csv_parquet(df, full_dest_path)

        print("file written to parquet")

    except Exception as err:
        print(err)



