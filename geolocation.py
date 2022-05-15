from numpy import unicode_
import requests, json
import pandas as pd
from unidecode import unidecode #pip install unidecode
import time;

of = open('geocodes.csv', "w+")
of.write('Country (Name),State/Province,City,Latitude,Longitude\n')

token = ''


with open('alba.csv', mode = 'r') as f:
    csvf = pd.read_csv(f)

    for loc in csvf['loc'].unique():
        l = unidecode(loc)
        url = 'https://us1.locationiq.com/v1/search.php?key={}&q={}%20Alba%20County&format=json'.format(token, l)
        resp = requests.get(url)
        print('Parsing response for city ' + loc)
        
        for obj in json.loads(resp.content):
            print(obj)
            if 'lat' in obj and 'lon' in obj:
                lat = obj['lat']
                long = obj['lon']
            else:
                lat = obj
                long = obj
                
            ol = 'Romania,Alba,{},{},{}\n'.format(loc, lat, long)
            of.write(ol)
            break
        time.sleep(1)
        
print("Cleaning data")

data = pd.read_csv('geocodes.csv')
data['City'] =  data['City'].str.capitalize()
data = data.drop_duplicates(subset=['City'], keep='first')
data = data.reset_index(drop=True)
data.to_csv('geocodes_deduped.csv', index=False)

print("done")

of.close()