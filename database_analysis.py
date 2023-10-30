from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, func

# Define the database connection URL (replace 'your_database_url' with the actual URL)
database_url = 'your_database_url'
engine = create_engine(database_url)

# Create a metadata object
metadata = MetaData()

# Define the 'track' table
track = Table(
    'track',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('Name', String),
    # ... other columns ...
)

# Establish a connection to the database
con = engine.connect()

# Construct a SQL SELECT statement using SQLAlchemy's expression language
stmt = select([func.count(track.columns.Name.distinct())])

# Execute the SQL statement against the database connection (con)
# Returns a ResultProxy, which can be used to fetch the results
results = con.execute(stmt).fetchall()

# Print the results obtained from the executed query
print(results)

# Close the database connection
con.close()
