import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import numpy as np

# Create a SQLite database
database_path = 'mydatabase.db'
engine = create_engine(f'sqlite:///{database_path}')

# Define the table schema
Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'mytable'
    id = Column(Integer, primary_key=True)
    dates = Column(String(255))
    orders = Column(Integer)
    transactions = Column(Integer)
    revenue = Column(Integer)
    margin = Column(Float)
    cvr = Column(Float)
    xf = Column(Integer)

# Create the table in the database
Base.metadata.create_all(engine)

# Generate random data for demonstration purposes
np.random.seed(42)
dates = pd.date_range(start='2023-08-15', periods=80, freq='D')
orders = np.random.randint(10, 100, size=80)
transactions = np.random.randint(10, 100, size=80)
revenue = np.random.randint(100, 1000, size=80)
margin = np.random.uniform(0.05, 0.12, size=80)
cvr = np.random.uniform(0.02, 0.12, size=80)
new_cst = np.random.randint(20, 450, size=80)

# Create a DataFrame
data = {
    'date': dates,
    'orders': orders,
    'transactions': transactions,
    'revenue': revenue,
    'margin': margin,
    'cvr': cvr,
    'new_cst': new_cst
}
df = pd.DataFrame(data)

# Insert the data into the table
df.to_sql('mytable', con=engine, if_exists='replace', index=False)

# Confirm the table creation
print(f"Table 'mytable' created successfully in the '{database_path}' database.")
