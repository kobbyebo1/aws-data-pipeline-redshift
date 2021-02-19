# aws-data-pipeline-redshift

Project Description: The aim of this project is to build a true source of historic data on stock market performance. This data will be fed into predictive machine learning algorithm to make well informed investment decisions. An ETL pipeline ingests the data from an API into S3 bucket, processes them using Lambda function, and loads the data back into a Data Lake on S3 in parquet format. From the data lake, the data is loaded into a Redshift Data Warehouse from where it is fed to other teams for analytics activities.
