!/usr/bin/env python
# coding: utf-8

# In[76]:


#import libraries
#!pip install kaggle
import kaggle

!kaggle datasets download ankitbansal06/retail-orders -f orders.csv


# In[77]:


#extract file from zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip') 
zip_ref.extractall() # extract file to dir
zip_ref.close() # close file


#read data from the file and handle null values


import pandas as pd
df = pd.read_csv('orders.csv',na_values=['Not Available','unknown'])
df['Ship Mode'].unique()




#rename columns names ..make them lower case and replace space with underscore
df.rename(columns={'Order Id':'order_id', 'City':'city'})
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')

df.head(5)

#discount coloumn
df['discount']=df['list_price']*df['discount_percent']*.01


#sale_price coloumn
df['sale_price']=df['list_price']-df['discount']

#profit coloumn
df['profit']=df['sale_price']- df['cost_price']


#convert order date from object data type to datetime
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")


#drop cost price list price and discount percent columns
df.drop(columns=['list_price','cost_price','discount_percent'],inplace= True)



#loading into the databasa

import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load your existing dataset (example for CSV)
df = pd.read_csv('--------')  # Load your DataFrame

# Step 2: Define your PostgreSQL connection parameters
username = '-------'          # Your PostgreSQL username
password = '-------'       # URL-encoded password if it contains special characters
hostname = 'localhost'         # Your database server's hostname
port = '------'                  # Default PostgreSQL port
database_name = '--------'          # Your database name

# Step 3: Create a connection to the PostgreSQL database
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}')

# Step 4: Transfer the DataFrame to PostgreSQL
try:
    df.to_sql('fresh_orders', con=engine, index=False, if_exists='append')
    print("Data transferred successfully.")
except Exception as e:
    print(f"Error: {e}")

# Optional: Close the connection
engine.dispose()
