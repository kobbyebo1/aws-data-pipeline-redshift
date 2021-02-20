
create schema stock_api;
commit;



CREATE TABLE IF NOT EXISTS stock_api.stocks_stage(
"date" varchar,
"symbol" varchar,
"open" FLOAT,
"high" FLOAT,             
"low" FLOAT,
"close" FLOAT,
"volume" FLOAT
);
commit;


copy stock_api.stocks_stage from 's3://our-data-lake-dev/'
iam_role 'arn:aws:iam::751250582587:role/RedshiftCopyUnload' 
FORMAT AS PARQUET;
commit;

