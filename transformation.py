import pandas as pd
import logging
from cassandra.cluster import Cluster
from sqlalchemy import inspect
from dagster import op, Out, In, get_dagster_logger
from dagster_pandas import PandasColumn, create_dagster_pandas_dataframe_type
from pymongo import MongoClient
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, exc
from sqlalchemy.pool import NullPool
from sqlalchemy.types import *

# Define the connection strings
postgres_connection_string = "postgresql://dap:dap@127.0.0.1:5432/electronic_items"
mongo_connection_string = "mongodb://127.0.0.1:27017"
logger = get_dagster_logger()

# Create the Dagster Pandas DataFrame type for Television
TelevisionDataFrame = create_dagster_pandas_dataframe_type(
    name="television",
    columns=[
        PandasColumn.string_column(name="Product_Name", non_nullable=True),
        PandasColumn.string_column(name="Stars", non_nullable=True),
        PandasColumn.string_column(name="Ratings", non_nullable=True),
        PandasColumn.string_column(name="Reviews", non_nullable=True),
        PandasColumn.float_column(name="current_price", non_nullable=True),
        PandasColumn.string_column(name="Operating_system", non_nullable=True),
        PandasColumn.float_column(name="MRP", non_nullable=True),
        PandasColumn.string_column(name="channel", non_nullable=True),
        PandasColumn.string_column(name="Picture_quality", non_nullable=True),
        PandasColumn.string_column(name="Speaker", non_nullable=True),
        PandasColumn.string_column(name="Frequency", non_nullable=True),
        PandasColumn.string_column(name="Image_url", non_nullable=True)
    ]
)

# Create the Dagster Pandas DataFrame type for Mobile
MobileDataFrame = create_dagster_pandas_dataframe_type(
    name="mobile",
    columns=[
        PandasColumn.string_column(name="phonename", non_nullable=True),
        PandasColumn.float_column(name="rating", non_nullable=True),
        PandasColumn.float_column(name="number_of_ratings", non_nullable=True),
        PandasColumn.string_column(name="ram", non_nullable=True),
        PandasColumn.string_column(name="rom", non_nullable=True),
        PandasColumn.string_column(name="front_camera", non_nullable=True),
        PandasColumn.string_column(name="battery", non_nullable=True),
        PandasColumn.string_column(name="processor"),
        PandasColumn.float_column(name="price", non_nullable=True),
    ]
)

# Create the Dagster Pandas DataFrame type for Laptop
LaptopDataFrame = create_dagster_pandas_dataframe_type(
    name="laptop",
    columns=[
        PandasColumn.integer_column(name="sno", non_nullable=True),
        PandasColumn.string_column(name="company", non_nullable=True),
        PandasColumn.string_column(name="type_name", non_nullable=True),
        PandasColumn.float_column(name="inches", non_nullable=True),
        PandasColumn.string_column(name="screen_resolution", non_nullable=True),
        PandasColumn.string_column(name="cpu", non_nullable=True),
        PandasColumn.string_column(name="ram", non_nullable=True),
        PandasColumn.string_column(name="memory", non_nullable=True),
        PandasColumn.string_column(name="gpu", non_nullable=True),
        PandasColumn.string_column(name="opsys", non_nullable=True),
        PandasColumn.float_column(name="weight", non_nullable=True),
        PandasColumn.float_column(name="price", non_nullable=True),
        PandasColumn.string_column(name="screen_resolution_type", non_nullable=True),
        PandasColumn.string_column(name="cpu_brand", non_nullable=True),
        PandasColumn.string_column(name="memory_type", non_nullable=True),
        PandasColumn.string_column(name="gpu_brand", non_nullable=True),
        PandasColumn.integer_column(name="opsys_encoded", non_nullable=True),
        PandasColumn.string_column(name="manufacturer", non_nullable=True),
        PandasColumn.string_column(name="screen_size_category", non_nullable=True),
        PandasColumn.integer_column(name="company_encoded", non_nullable=True)
    ]
)

# Set up logger
logger = logging.getLogger(__name__)

@op(
    ins={"start": In(bool)},
    out=Out(TelevisionDataFrame)
)
def transform_Television(start):
    try:
        # Connect to the MongoDB database
        client = MongoClient(mongo_connection_string)
        television_db = client["television"]
        television_collection = television_db["television"]

        # Retrieve data from MongoDB collection
        television_data = list(television_collection.find())

        if not television_data:
            logger.warning("No data retrieved from the MongoDB collection")
            return pd.DataFrame()  # Return an empty DataFrame

        # Convert data to DataFrame
        television_df = pd.DataFrame(television_data)
        television_df['current_price'] = television_df['current_price'].str.replace('\u00e2\u201a\u00b9', '').astype(float)
        television_df['MRP'] = television_df['MRP'].str.replace('\u00e2\u201a\u00b9', '').astype(float)
     
        # Ensure all column names are strings
        television_df.columns = television_df.columns.astype(str)

        # Clean column names
        television_df.columns = television_df.columns.str.replace('[^a-zA-Z0-9]', '_')

        # Handle missing values
        television_df = television_df.dropna()

        # Check if 'Product_Name' column exists before proceeding
        if 'Product_Name' not in television_df.columns:
            logger.error("'Product_Name' column not found in DataFrame. Available columns: %s", television_df.columns.tolist())
            return pd.DataFrame()  # Return an empty DataFrame

        # Other transformations...
        return television_df

    except Exception as e:
        logger.error("Error occurred during data transformation: %s", str(e))
        return pd.DataFrame()  # Return an empty DataFrame

engine = create_engine("sqlite:///LaptopDB.db")

# Define metadata
metadata = MetaData()

# Define the table schema
laptop_table = Table(
    "LaptopTable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sno", Integer),
    Column("company", String),
    Column("type_name", String),
    Column("inches", Float),
    Column("screen_resolution", String),
    Column("cpu", String),
    Column("ram", String),
    Column("memory", String),
    Column("gpu", String),
    Column("opsys", String),
    Column("weight", Float),
    Column("price", Float),
    Column("screen_resolution_type", String),
    Column("cpu_brand", String),
    Column("memory_type", String),
    Column("gpu_brand", String),
    Column("opsys_encoded", Integer),
    Column("manufacturer", String),
    Column("screen_size_category", String),
    Column("company_encoded", Integer),
)

# Create all tables
metadata.create_all(engine)


# Configure logger
logger = logging.getLogger(__name__)

@op(
    ins={"start": In(bool)},
    out=Out(MobileDataFrame)
)
def transform_Mobile(start):
    try:
        # Connect to the Cassandra cluster
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('mobile')

        # Execute a CQL query to retrieve data from the mobile table
        query = "SELECT * FROM mobile"
        mobile_df = pd.DataFrame(list(session.execute(query)))
        print(mobile_df.columns,'mobile_df')
        # Clean column names
        mobile_df.columns = mobile_df.columns.str.replace('[^a-zA-Z0-9]', '_')
        # Handle missing values
        mobile_df = mobile_df.dropna()
        
        # Check if the 'phonename' column exists
       
        print(mobile_df.columns,'mobile_df')
        return mobile_df

    except Exception as e:
        logger.error("Error occurred while transforming Mobile data: %s", str(e))
        # Return an empty DataFrame or raise an error depending on your requirement
        return pd.DataFrame()

@op(
    ins={"start": In(bool)},
    out=Out(LaptopDataFrame)
)
def transform_Laptop(start):
    try:
        # Connect to the SQL database
        engine = create_engine("sqlite:///LaptopDB.db")

        # Check if the table exists
        inspector = inspect(engine)
        if not inspector.has_table("LaptopTable"):
            raise Exception("LaptopTable does not exist in the database.")

        # Retrieve data from SQL table
        laptop_df = pd.read_sql("SELECT * FROM LaptopTable", engine)

        # Clean column names
        laptop_df.columns = laptop_df.columns.str.replace('[^a-zA-Z0-9]', '_')

        # Handle missing values
        laptop_df = laptop_df.dropna()

          # Convert 'sno' column to integer data type
        laptop_df['sno'] = laptop_df['sno'].astype(int)

         # Convert 'inches' column to float data type
        laptop_df['inches'] = laptop_df['inches'].astype(float)
        laptop_df['weight'] = laptop_df['weight'].astype(float)

        laptop_df['price'] = laptop_df['price'].astype(float)
         # Convert 'opsys_encoded' column to integer data type

        laptop_df['opsys_encoded'] = laptop_df['opsys_encoded'].astype(int)

        # Convert 'company_encoded' column to integer data type
        laptop_df['company_encoded'] = laptop_df['company_encoded'].astype(int)

        return laptop_df

    except Exception as e:
        logger.error(f"Error occurred while transforming Laptop data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error
    


@op(
    ins={"television_df": In(pd.DataFrame), "mobile_df": In(MobileDataFrame), "laptop_df": In(LaptopDataFrame)},
    out=Out(pd.DataFrame)
)
def merge_data_frames(television_df, mobile_df, laptop_df):
    # Merge data frames

    merged_df = television_df.merge(
        right = mobile_df,
        how="left",
        left_on="MRP",
        right_on="price"
    )
    
    merged_quality_df = merged_df.merge(
        right=laptop_df,
        how="left",
        left_on="price",
        right_on="price"
    )
    merged_quality_df.drop(["_id"],axis=1,inplace=True)
    merged_quality_df.drop(["date_of_scraping"],axis=1,inplace=True)
    # Drop the datetime column as we already have a date column
    # merged_quality_df.drop(["state.area"],axis=1,inplace=True)
    
    # Return the joined data frames
    return(merged_quality_df)


@op(
    ins={"merged_quality_df": In(pd.DataFrame)},
    out=Out(bool)
)
def load_to_postgres(merged_quality_df):
    try:
        print(merged_quality_df.dtypes,'popkl')
        # Create a connection to the PostgreSQL database
        engine = create_engine(
            postgres_connection_string,
            poolclass=NullPool
        )

        
       
        # created database. We will change some of these types later.
        database_datatypes = dict(zip(merged_quality_df.columns,[VARCHAR]*len(merged_quality_df.columns)))
        
        # Set date column to have the TIMESTAMP datatype
        # database_datatypes["date"] = TIMESTAMP
        

        # Set columns with DOUBLE PRECISION datatype
        for column in ["current_price","MRP","rating","number_of_ratings","price","inches","weight", "sno", "company_encoded"]:
            database_datatypes[column] = DECIMAL
    
            
        # Open the connection to the PostgreSQL server
        with engine.connect() as conn:
            
            # Store the data frame contents to the flight_weather 
            # table, using the dictionary of data types created
            # above and replacing any existing table
            rowcount = merged_quality_df.to_sql(
                name="electronices_merged",
                schema="public",
                dtype=database_datatypes,
                con=engine,
                index=False,
                if_exists="replace"
            )
            logger.info("{} records loaded".format(rowcount))
            
        # Close the connection to PostgreSQL and dispose of 
        # the connection engine
        engine.dispose(close=True)
        
        # Return the number of rows inserted
        return rowcount > 0
    
    # Trap and handle any relevant errors
    except exc.SQLAlchemyError as error:
        logger.error("Error: %s" % error)
        return False


