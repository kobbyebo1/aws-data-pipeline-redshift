# aws-data-pipeline-redshift

**Project Description**: The aim of this project is to build a true source of historic data on stock market performance. This data will be fed into predictive machine learning algorithm to make well informed investment decisions. An ETL pipeline ingests the data from an API into S3 bucket, processes them using Lambda function, and loads the data back into a Data Lake on S3 storage in parquet format. From the data lake, the data is loaded into a Redshift Data Warehouse from where it is fed to other teams for analytics activities.


## Data description

The dataset is extracted from the API (https://www.alphavantage.co) using a scheduled script running on EC2 instance. The raw data which is in the JSON format is pre-processed in the script into csv files that are stored in S3 bucket by date prefix.

The data resides in the following s3 bucket.
stocks data: s3://<landing zone>/<timestamp>.csv
  

**Original JSON format of data from API**
{
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "IBM",
        "3. Last Refreshed": "2021-02-18",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2021-02-18": {
            "1. open": "120.5000",
            "2. high": "120.9400",
            "3. low": "119.7000",
            "4. close": "120.7300",
            "5. volume": "5399145"
        },
        "2021-02-17": {
            "1. open": "119.2700",
            "2. high": "120.5600",
            "3. low": "119.0200",
            "4. close": "119.9700",
            "5. volume": "3949876"
        },


**Pre-processed data format after extraction**
JSON data is stored in S3 landing zone in csv format below.

	symbol	date	1. open	2. high	3. low	4. close	5. volume
0	IBM	2021-02-17	119.27	120.56	119.02	119.97	3949876.0
1	IBM	2021-02-16	120.15	120.6	119.36	120.07	6639790.0
2	IBM	2021-02-12	121.0	121.36	120.09	120.8	3871195.0
3	IBM	2021-02-11	122.0	122.205	120.63	120.91	5381556.0
4	IBM	2021-02-10	123.03	123.41	121.2138	122.24	4831858.0



## Project Structure

etl.py: The script runs on EC2 and reads stocks data from API on a daily schedule, transforms them and writes them to csv files into landing zone on S3.
lambda.py: Event trigged script that processes csv files that are dropped into landing zone and compresses them into parquet file format in data lake on S3.
dl.cfg: Contains credentials for accessing S3.
redshift.sql: Creates a schema and table in Redshift to hold the data that is copied from S3.
landing zone data: A sample of stocks data saved locally for testing before going to S3.
data lake data: A sample of processed stocks data stored in data lake in compressed parquet format.

## Methodology

etl.py script starts off by reading stocks from API, transforms them into tabular format as stores them as csv files on S3 landing zone. A limited number of random stocks symbos is used for simplicty of the project. This script is scheduled on a linux EC2 instance using cronjobs and runs daily to retrieve updated information.


Once the csv files hit the landing zone, it triggers a lambda function to run and process the files further and stores them back on S3 data lake in a parquet compressed format.


Data from the columnar parquet files are then loaded into a table on Redshift Data Warehouse.



