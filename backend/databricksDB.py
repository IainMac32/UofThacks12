from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def upload_to_db(main_topic,slide_link):
    # Step 1: Initialize SparkSession with Delta support
    builder = SparkSession.builder \
        .appName("DeltaLakeExample") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Step 2: Create a DataFrame and save it as a Delta table
    data = [{"user_topic": main_topic, 'slide_link': slide_link}]
    df = spark.createDataFrame(data)

    df.write.format("delta").mode("append").save("delta-table")
    return


def retrieve_from_db():
    # Step 1: Initialize SparkSession with Delta support
    builder = SparkSession.builder \
        .appName("DeltaLakeExample") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Step 3: Read from the Delta table
    delta_df = spark.read.format("delta").load("delta-table")
    delta_df.show()

    # Retrieve data as a list of dictionaries
    result = [row.asDict() for row in delta_df.collect()]
    return result




