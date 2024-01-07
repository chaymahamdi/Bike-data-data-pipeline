import json
import time
import requests
from kafka import KafkaProducer
from datetime import datetime 

API_KEY = "768abbc098e4e65930e4f68f7c2c85f43f420d53"  # url for velib_stations

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
base_url = 'https://api.jcdecaux.com/vls/v1/'
endpoint = 'stations'
country_code = 'FR'
url = f'{base_url}{endpoint}?country_code={country_code}&apiKey={API_KEY}'
        
while True:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for line in data:
                print("reading data")
                utcfromtimestamp = datetime.utcfromtimestamp(int(line['last_update'])/1000).strftime('%Y-%m-%d %H:%M:%S')

                data_structure = {
                    'numbers': line['number'],
                    'contract_name': line['contract_name'],
                    'banking': line['banking'],
                    'bike_stands': line['bike_stands'],
                    'available_bike_stands': line['available_bike_stands'],
                    'available_bikes': line['available_bikes'],
                    'address': line['address'],
                    'status': line['status'],
                    'position': line['position'],
                    'last_update': utcfromtimestamp
                }

                producer.send('velib-stations', value=data_structure)
                print(data_structure)
                time.sleep(2)
        else:
            print(f'Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print("Error:", str(e))
    time.sleep(10)

