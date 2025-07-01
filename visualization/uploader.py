import csv
import requests

ELASTIC_URL = "http://elasticsearch:9200"
INDEX = "incidentes"

def create_index():
    r = requests.put(f"{ELASTIC_URL}/{INDEX}")
    if r.status_code not in [200, 201]:
        print("El índice puede que ya exista o hubo un error:", r.text)

def upload_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = requests.post(f"{ELASTIC_URL}/{INDEX}/_doc", json=row)
            print(r.status_code, r.reason)

if __name__ == "__main__":
    create_index()
    upload_csv("/data/clean/incidents_clean.csv")
