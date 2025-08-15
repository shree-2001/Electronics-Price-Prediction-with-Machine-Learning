from dagster import job
from extract import *
from transformation import *
from Visualization import *

@job
def etl():
        
        # Load the joined data into PostgreSQL
        load_to_postgres(
            # Join the flights and weather data
            merge_data_frames(
                # Transform the stored flights data
                transform_Television(
                    # Extract and store the flights data
                    extract_Television()
                ),
                # Transform the stored weather data
                transform_Mobile(
                    # Extract and store the weather data
                    extract_mobile()
                ),
                transform_Laptop(
                    # Extract and store the weather data
                    extract_laptop()
                )
            )
        )
  