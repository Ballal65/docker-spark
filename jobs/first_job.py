import os
from pyspark.sql import SparkSession


def log_directory_contents():
    """Log contents of key directories for debugging."""
    directories = [
        '/opt/', 
        '/opt/airflow', 
        '/opt/shared/extracted_data', 
        '/opt/shared/extracted_data/youtube_data'
    ]
    
    for dir_path in directories:
        try:
            print(f"Contents of {dir_path}: {os.listdir(dir_path)}")
        except Exception as e:
            print(f"Error accessing {dir_path}: {e}")

def main():
    # Log directory contents for diagnostics
    log_directory_contents()

    input_path = '/opt/shared/extracted_data/youtube_data/jre_data_2025-01-23.csv'
    output_path = '/opt/shared/transformed_data/youtube_data/jre_title.csv'

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    spark = None
    try:
        # Create Spark Session with more robust configuration
        spark = SparkSession.builder \
            .appName("YouTubeDataTransformation") \
            .config("spark.executor.memory", "1g") \
            .config("spark.driver.memory", "1g") \
            .config("spark.sql.shuffle.partitions", "200") \
            .config("spark.executor.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
            .config("spark.driver.extraJavaOptions", "--add-opens java.base/java.nio=ALL-UNNAMED") \
            .getOrCreate()
        
        # Set log level for more detailed tracking
        spark.sparkContext.setLogLevel("INFO")
        print("SparkSession initialized successfully")

        # Robust file reading with additional options
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("multiline", "true") \
            .option("escape", '"') \
            .csv(input_path)

        # Log DataFrame details
        print(f"Total records: {df.count()}")
        print(f"DataFrame schema: {df.schema}")

        # Show first few records
        df.show(5)

        # Select and save titles
        output_df = df.select("Title")
        output_df.write.mode("overwrite").csv(output_path)

        print(f"Titles extracted and saved to {output_path}")

    except FileNotFoundError:
        print(f"Input file not found: {input_path}")
    except Exception as e:
        print(f"Error during Spark job execution: {e}", exc_info=True)
    finally:
        if spark:
            spark.stop()

if __name__ == "__main__":
    main()