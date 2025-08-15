import json
import pandas as pd
from cassandra.cluster import Cluster
from pymongo import MongoClient
from dagster import op, Out, get_dagster_logger
import datetime

logger = get_dagster_logger()

# Parameters for MongoDB connection and file paths
MONGO_CONNECTION_STRING = "mongodb://127.0.0.1:27017"
TELEVISION_JSON_FILE = "Television.json"
MOBILE_CSV_FILE = "mobile_prices.csv"
LAPTOP_CSV_FILE = "laptop_data.csv"

# Parameters for Cassandra connection
CASSANDRA_ENDPOINTS = ["127.0.0.1"]
KEYSPACE_TELEVISION = "television"
KEYSPACE_MOBILE = "mobile"
KEYSPACE_LAPTOP = "laptop"


def connect_to_cassandra(keyspace):
    try:
        cassandra = Cluster(CASSANDRA_ENDPOINTS)
        session = cassandra.connect(keyspace)
        return session
    except Exception as e:
        logger.error(f"Error connecting to Cassandra keyspace '{keyspace}': {e}")
        raise


@op(out=Out(bool))
def extract_Television() -> bool:
    try:
        logger.info("Starting extraction of Television data...")
        client = MongoClient(MONGO_CONNECTION_STRING)
        electronic_items_db = client["television"]
        television_collection = electronic_items_db["television"]
        television_collection.drop()
        with open(TELEVISION_JSON_FILE, "r") as fh:
            data = json.load(fh)
        for television in data: # Iterate over each television object in the list
            try:
                print(television,'television_pop')
                
                transformed_television = {"Product_Name": television["Product_Name"],"Stars": television["Stars"], "Ratings": television["Ratings"], "Reviews": television["Reviews"], "current_price": television["current_price"], "Operating_system": television["Operating_system"], "MRP": television["MRP"],"channel": television["channel"],"Picture_quality": television["Picture_qualtiy"],"Speaker": television["Speaker"],"Frequency": television["Frequency"],"Image_url": television["Image_url"] }
                print(transformed_television,'transformed_television_pop')
                television_collection.insert_one(transformed_television)
                
                  
            except errors.DuplicateKeyError as err:
                print('duplicate')
                logger.error("Error: %s" % err)
                continue
        return True
    except Exception as e:
        logger.error(f"Error extracting Television data: {e}")
        return False


@op(out=Out(bool))
def extract_laptop() -> bool:
    try:
        logger.info("Starting extraction of Laptop data...")
        laptop_df = pd.read_csv(LAPTOP_CSV_FILE)
        laptop_df.columns = ['sno', 'company', 'typename', 'inches',
                             'screenresolution', 'cpu', 'ram', 'memory', 'gpu',
                             'opsys', 'weight', 'price']

        # Convert Weight column to float, replacing any non-numeric values with NaN
        laptop_df['weight'] = pd.to_numeric(laptop_df['weight'], errors='coerce')

        session = connect_to_cassandra(KEYSPACE_LAPTOP)

        session.execute(
            """
            CREATE TABLE IF NOT EXISTS laptop(
                sno INT PRIMARY KEY,
                company TEXT,
                typename TEXT,
                inches FLOAT,
                screenresolution TEXT,
                cpu TEXT,
                ram TEXT,
                memory TEXT,
                gpu TEXT,
                opsys TEXT,
                weight FLOAT,
                price FLOAT
            )
            """
        )

        prepared_insert = session.prepare(
            """
            INSERT INTO laptop (sno, company, typename, inches, screenresolution,
                                cpu, ram, memory, gpu, opsys, weight, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )

        for _, row in laptop_df.iterrows():
            session.execute(prepared_insert, tuple(row))

        logger.info("Laptop data extraction completed.")
        return True

    except Exception as e:
        logger.error(f"Error extracting Laptop data: {e}")
        return False


def connect_to_cassandra(keyspace):
    try:
        cassandra = Cluster(CASSANDRA_ENDPOINTS)
        session = cassandra.connect(keyspace)
        return session
    except Exception as e:
        logger.error(f"Error connecting to Cassandra keyspace '{keyspace}': {e}")
        raise

@op(out=Out(bool))
def extract_mobile() -> bool:
    try:
        logger.info("Starting extraction of Mobile data...")
        mobile_df = pd.read_csv(MOBILE_CSV_FILE, delimiter=',')
        print(mobile_df,'mass')
        mobile_df.columns = ["phonename","rating","number_of_ratings","ram","rom","front_camera","battery","processor","price","date_of_scraping"]
        print(mobile_df,'matt')
        # Remove currency symbol and commas from 'price' column and convert to float
        mobile_df['price'] = mobile_df['price'].str.replace('₹', '').str.replace(',', '')
        mobile_df['number_of_ratings'] = mobile_df['number_of_ratings'].str.replace(',', '').astype(float)
    
        # Convert 'price' column to float
        mobile_df['price'] = mobile_df['price'].astype(float)
        print(mobile_df,'vit')
        session = connect_to_cassandra(KEYSPACE_MOBILE)

        session.execute(
            """
            DROP TABLE IF EXISTS mobile
            """
        )

        session.execute(
            """
            CREATE TABLE IF NOT EXISTS mobile(
                phonename TEXT PRIMARY KEY,
                rating FLOAT,
                number_of_ratings FLOAT,
                ram TEXT,
                rom TEXT,
                front_camera TEXT,
                battery TEXT,
                processor TEXT,
                price FLOAT,
                date_of_scraping DATE
            )
            """
        )
        print('10')

        prepared_insert = session.prepare(
            """
            INSERT INTO mobile (phonename, rating, number_of_ratings, ram,
                                rom, front_camera, battery,
                                processor, price, date_of_scraping)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        print('10')
        for index, row in mobile_df.iterrows():
            # Convert the row values to a list
            array = []
            
            row_values = row.values.flatten().tolist()
            for ris in row_values:
                array.append(ris)
            print(array,'array...')
            session.execute(prepared_insert, array)

        logger.info("Mobile data extraction completed.")
        return True

    except Exception as e:
        logger.error(f"Error extracting Mobile data: {e}")
        return False