from pyspark.sql import SparkSession
import os

def main():
    # Initialize SparkSession
    print("Starting the Spark job...")
    try:
        print("Contents of /opt/")
        print(os.listdir('/opt'))
        print("Contents of /opt/airflow")
        print(os.listdir('/opt/airflow'))
        print("Contents of /opt/airflow/extracted_data:")
        print(os.listdir('/opt/airflow/extracted_data'))
        print("Contents of /opt/airflow/extracted_data/youtube_data:")
        print(os.listdir('/opt/airflow/extracted_data/youtube_data'))
    except Exception as e:
        print(f"Error accessing directories: {e}")


    #input_path = '/opt/airflow/extracted_data/youtube_data/jre_2025-01-22.csv'
    input_path = '/opt/airflow/extracted_data/youtube_data/jre_data_2025-01-23.csv'
    output_path = '/opt/airflow/transformed_data/youtube_data/jre_title.csv'

    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return

    spark = SparkSession.builder \
    .appName("SimpleTransformation1") \
    .config("spark.executor.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
    .config("spark.driver.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
    .getOrCreate()

    try:
        # Read the input file
        print(f" \n \n \n \n \n \n Hello world {os.listdir()} \n \n \n \n ")
        df = spark.read.csv(input_path, header=True, inferSchema=True)

        # Select a single column
        output_df = df.select("Title")
        pandas_df = output_df.toPandas()
        pandas_df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"Error occurred during Spark job execution: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()