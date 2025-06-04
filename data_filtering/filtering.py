import pandas as pd
from pymongo import MongoClient
import os
import time

def clean_and_standardize(mongo_uri, db_name, collection_name, output_path):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    if df.empty:
        print("No se encontraron datos en MongoDB.")
        return

    df.drop_duplicates(subset=["alert_id"], inplace=True)

    df["region_name"] = df["region_name"].str.strip().str.lower()
    df["type"] = df["type"].str.strip().str.upper()

    df["comuna"] = df["comuna"]


    df["descripcion"] = "Alerta de tipo " + df["type"] + " reportada por " + df["report_by"]

    output_columns = ["type", "comuna", "descripcion", "report_rating", "location_x", "location_y"]
    df = df[output_columns]

    df.to_csv(output_path, index=False)
    print(f"[OK] Datos limpios guardados en {output_path}")

if __name__ == "__main__":
    mongo_uri = "mongodb://dumbuser:dumbpassword@mongo:27017"
    db_name = os.getenv("MONGO_DB", "admin")
    collection_name = os.getenv("MONGO_COLLECTION", "alerts")
    output_file = os.getenv("OUTPUT_FILE", "/data/clean/incidents_clean.csv")

    clean_and_standardize(mongo_uri, db_name, collection_name, output_file)
