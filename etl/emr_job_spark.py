from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("ExerciseSpark")
    .getOrCreate()
)

# Ler os dados da RAIS 2020
enem = (
    spark
    .read
    .format("txt")
    .option("header", True)
    .option("inferSchema", True)
    .option("delimiter", ";")
    .load("s3://igti-eric-rais2020-mod1/raw/")
)

(
    enem
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3://igti-eric-rais2020-mod1/staging-zone/")
)
