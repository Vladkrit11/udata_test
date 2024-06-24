import json
import os


with open('scrape_rent/output.json') as f:
    data = json.load(f)

for item in data:
    country = 'Germany'
    domain = item['url'].split('/')[2]
    rental_object = item['title'].replace('/', '-').replace('\\', '-')

    os.makedirs(f'{country}/{domain}/{rental_object}', exist_ok=True)

    with open(f'{country}/{domain}/{rental_object}/data.json', 'w') as f:
        json.dump(item, f, indent=4)
