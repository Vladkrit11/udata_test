To start:
Activate venv: venv/Scripts/activate
Install requirements: pip install -r requirements.txt
To parse data: 
cd scrape_rent
scrapy crawl kelm -o output.json
To sort data: run >> organized_out.py

IMPORTANT: I ​​could not parse images because Scrapy cannot work with JavaScript scripts, and Splash did not give the required result. Thank you for your time and understanding :)
