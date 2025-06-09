# wttj-bot-v2

## Create a virtual env

```
python3 -m venv venv
source venv/bin/activate
```

## Install requirements

`pip install -r requirements.txt`

## Fill your motivation_letter.txt

## Fill your blacklist.txt

The format is:

```
google
meta
netflix
ect
```

## Create an .env file

It should contains

```
EMAIL=...
PASSWORD="..."
QUERIES='["backend", "frontend"]'
REGION=rouen
```

## Run wttj_getter.py

`python3 wttj_getter.py` (don't forget to activate the virtual env)

You would get a list of the scrapped enterprises in enterprises.json

## Run wttj_sender.py

`python3 wttj_sender.py` (don't forget to activate the virtual env)