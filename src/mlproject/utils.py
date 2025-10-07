import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pymysql
from pymongo import MongoClient
import pickle
import numpy as np
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv('db')


mongo_uri = os.getenv("mongo_uri")
db_name = os.getenv("db_name")
collection_name = os.getenv("collection_name")


def read_mongo_data():
    logging.info("Reading MongoDB database started...")
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        logging.info(f"✅ Connection Established to MongoDB: {mongo_uri}")

        # Read data from MongoDB collection
        data = list(collection.find())
        if not data:
            logging.warning("⚠️ No data found in the collection.")
            return pd.DataFrame()

        # Convert to pandas DataFrame
        df = pd.DataFrame(data)

        # Optional: remove MongoDB ObjectId column
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        print(df.head())

        return df

    except Exception as ex:
        logging.error(f"❌ Error reading MongoDB data: {ex}")
        raise CustomException(ex)

    finally:
        client.close()
        logging.info("🔒 MongoDB connection closed.")


def read_sql_data():
    logging.info("Reading SQL database started")
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        #logging.info("Connection Established",mydb)
        logging.info(f"Connection Established: {mydb}")
        df=pd.read_sql_query('Select * from students',mydb)
        print(df.head())

        return df



    except Exception as ex:
        raise CustomException(ex)
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
