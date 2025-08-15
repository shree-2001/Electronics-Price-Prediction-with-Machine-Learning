import pandas.io.sql as sqlio
import psycopg2
from dagster import op, In
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, event, text, exc
from sqlalchemy.engine.url import URL

@op(
    ins={"start": In(bool)}
)

def visualise(start):
    
    postgres_connection_string = "postgresql://dap:dap@127.0.0.1:5432/Electronic_Items"

    # A query to return the number of minutes delay in departures and the rainfall
    query_string = """
    SELECT * FROM merged_data;
    """

    try:
        # Connect to the PostgreSQL database
        engine = create_engine(postgres_connection_string)     
        # Run the query and return the results as a data frame
        with engine.connect() as connection:
            electronic_dataframe = sqlio.read_sql_query(
                text(query_string), 
                connection
            )
        TOOLS = """hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,
            box_zoom,reset,tap,save,box_select,poly_select,
            lasso_select"""

        # Create a Bokeh figure
        plt.figure(figsize=(12, 8))

        # Scatter plot
        plt.subplot(2, 2, 1)
        sns.scatterplot(x='origin_current_price', y='origin_MRP', data=df)
        plt.title('Scatter Plot')
        plt.xlabel('Current Price')
        plt.ylabel('MRP')

        # Bar chart
        plt.subplot(2, 2, 2)
        sns.countplot(x='origin_mobile_brands', data=df)
        plt.title('Bar Chart')
        plt.xlabel('Mobile Brands')
        plt.ylabel('Count')

        # Box plot
        plt.subplot(2, 2, 3)
        sns.boxplot(x='screen_size_category', y='price', data=df)
        plt.title('Box Plot')
        plt.xlabel('Screen Size Category')
        plt.ylabel('Price')

        # Pair plot
        plt.subplot(2, 2, 4)
        sns.pairplot(electronic_dataframe[['inches', 'price', 'weight', 'origin_Back_camera']])
        plt.title('Pair Plot')

       # Adjust layout
        plt.tight_layout()

       # Show plot
        plt.show()
    except exc.SQLAlchemyError as dbError:
        print ("PostgreSQL Error", dbError)
    finally:
        if engine in locals(): 
            engine.close()