# Databricks notebook source
dbutils.fs.rm("dbfs:/babynames.csv")

# COMMAND ----------

import urllib3
response = urllib3.PoolManager().request('GET', 'http://health.data.ny.gov/api/views/myeu-hzra/rows.csv')
csvfile = response.data.decode("utf-8")
dbutils.fs.put("dbfs:/babynames.csv", csvfile)

# COMMAND ----------

babynames = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("dbfs:/babynames.csv")
babynames.createOrReplaceTempView("babynames_table")

# COMMAND ----------

years = spark.sql("select distinct(Year) from babynames_table").rdd.map(lambda row : row[0]).collect()
years.sort()

# COMMAND ----------

dbutils.widgets.dropdown("year", "2014", [str(x) for x in years])

# COMMAND ----------

display(babynames.filter(babynames.Year == getArgument("year")))

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from babynames_table where Year = getArgument("year")
