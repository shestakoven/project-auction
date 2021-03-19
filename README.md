# Auction "PyCamp"

Here you can sell, buy, change and discuss things, goods, real estate, business - 
everything that has a price and can be sold.

At the auction, the thing becomes a commodity-lot, interested buyers, as in the
real market, offer their prices, bargain. Whoever offers more money or decides
to buy goods at a blitz price (that is, immediately) picks up the goods at a
convenient time and place. It is customary for us to bargain and discuss the
goods.

We created an auction in order to make the process of transferring a thing that
for some reason you no longer need, but may still be needed by someone, was
simple, useful and fun.

# Start

## Install requirements

```bash
$ pip install -r requirements/development.txt
```

## Run a database

```bash
$ docker-compose up -d postgres
```

## Apply migrations

```bash
$ ./manage.py migrate
```

## Run server

```bash
$ ./manage.py runserver
```

## Run Celery

```bash
$ celery --app config.celery:app worker -l info
```

```bash
$ celery --app config.celery:app beat -l info -S django
```

## Fill db some data

You can fill db some fake data

```bash
$ ./manage.py fill_db_sample_data
```

## Structure of project

The project consists of three applications: users, messages, marketplace.

### Users

The messaging app implements the logic of communication between users in
private messages. The application has one table that stores the correspondence
between users, as well as notifications from the site.

### Messages

The users application is designed to register a user profile and store his
personal data, such as name, surname, mail, phone number, avatar.

### Marketplace

The trading platform application implements the logic of interaction with lots.
There are five tables in the appendix: product categories, rates, lots,
comments under lots, product images. 


## Initial data

- `google_categories.xls` - this file is used on the data migration to 
  populate the Category table. File took from 
  [google categories](https://support.google.com/merchants/answer/6324436?hl=en).

## Add or update categories

To update or add new categories use command. The file structure must 
correspond to the "google_categories.xls" file. 
```bash
$ ./manage.py sync_categories_from_file_to_db -p path-to-file.xls
```