# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <span><img src= "https://cdn.oreillystatic.com/images/sitewide-headers/oreilly_logo_mark_red.svg"/>&nbsp;&nbsp;<font size="16"><b>Delta Lake: Up and Running<b></font></span>
# MAGIC 
# MAGIC  
# MAGIC  Name:          chapter 03/04 - The DataFrameWriter API
# MAGIC  
# MAGIC      Author:    Bennie Haelen
# MAGIC      Date:      12-10-2022
# MAGIC      Purpose:   The notebooks in this folder contains the code for chapter 3 of the book - Basic Operations on Delta Tables.
# MAGIC                 This notebook illustrates how to use the DataFrameWriter API to create Delta tables
# MAGIC 
# MAGIC                 
# MAGIC      The following Delta Lake functionality is demonstrated in this notebook:
# MAGIC        1 - Drop the taxidb.rateCard table
# MAGIC        2 - Read a CSV file into a DataFrame from the input path
# MAGIC        3 - Write the DataFrame to a managed Delta Table
# MAGIC        4 - Perform a DESCRIBE EXTENDED on the table to make sure that it is a managed table
# MAGIC        5 - Perform a SELECT on the table to ensure that the data was successfully loaded from the .csv input file
# MAGIC        6 - Drop the rateCard table so that you can re-created it as an unmanaged table
# MAGIC        7 - Write our DataFrame to your output path location
# MAGIC        8 - Create an unmanaged Delta table on top of the Delta File written in the previous step
# MAGIC        8 - Perform a SQL SELECT to show the records in the unmanaged table
# MAGIC 
# MAGIC    

# COMMAND ----------

INPUT_PATH = '/databricks-datasets/nyctaxi/taxizone/taxi_rate_code.csv'
DELTALAKE_PATH = 'dbfs:/mnt/datalake/book/chapter03/createDeltaTableWithDataFrameWriter'

# COMMAND ----------

# MAGIC %md
# MAGIC ###1 - Drop the taxidb.rateCard table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- You will be re-creating the taxidb.rateCard table from a .CSV
# MAGIC -- file, so you first need to drop it here
# MAGIC drop table if exists taxidb.rateCard;

# COMMAND ----------

# MAGIC %md
# MAGIC ###2 - Read in our taxi_rate_code.csv file 

# COMMAND ----------

# Read the Dataframe from the input path
df_rate_codes = spark                                              \
                .read                                              \
                .format("csv")                                     \
                .option("inferSchema", True)                       \
                .option("header", True)                            \
                .load(INPUT_PATH)

display(df_rate_codes)

# COMMAND ----------

# MAGIC %md
# MAGIC ###3 - Write the DataFrame as a managed Delta table

# COMMAND ----------

# Save our DataFrame as a managed Delta table
# You know that the table is managed since no location path was 
# specified
df_rate_codes.write.format("delta").saveAsTable('taxidb.rateCard')

# COMMAND ----------

# MAGIC %md
# MAGIC ###4 - Do a DESCRIBE EXTENDED on the rateCard managed table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- You can see that this is a managed table when
# MAGIC -- you run a DESCRIBE EXTENDED on the table
# MAGIC DESCRIBE TABLE EXTENDED taxidb.rateCard;

# COMMAND ----------

# MAGIC %md
# MAGIC ###5 - Peform a SELECT on the table to ensure that the data was successfully loaded from the .CSV file

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from taxidb.rateCard

# COMMAND ----------

# MAGIC %md
# MAGIC ###6 - Delete the rateCard table, we will re-created it as an unmanaged table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Drop the existing table
# MAGIC drop table if exists taxidb.rateCard;

# COMMAND ----------

# MAGIC %md
# MAGIC ###7 - Write our DataFrame to the output Data Lake Path

# COMMAND ----------

# Next, write out the data frame to our Data Lake Path, 
# this will create our Delta Files in that location
df_rate_codes                     \
        .write                    \
        .format("delta")          \
        .mode("overwrite")        \
        .save(DELTALAKE_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ###8 - Create an unmanaged Delta Table on top of the Delta File

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Finally, you create an unmanaged table on top of the Data Lake Path
# MAGIC -- Because we are specifying a LOCATION we know this is an unmanaged
# MAGIC -- table
# MAGIC CREATE OR REPLACE TABLE taxidb.rateCard
# MAGIC (
# MAGIC     RateCodeID   INT,
# MAGIC     RateCodeDesc STRING
# MAGIC )
# MAGIC LOCATION 'dbfs:/mnt/datalake/book/chapter03/createDeltaTableWithDataFrameWriter'

# COMMAND ----------

# MAGIC %md
# MAGIC ###9 - Display the records in the table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Perform a select from our unmanaged table
# MAGIC select * from taxidb.rateCard
