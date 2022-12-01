# Letterboxd to Ratehouse Migrator

A script for migrating your data from [Letterboxd](https://letterboxd.com) to [rate.house](https://rate.house/).

## Features
Currently supported migrations are:
- Ratings
- Watchlist

## Prerequisites
You must have a working [Google Chrome](https://www.google.com/intl/en_uk/chrome/) installation.

## Usage
First export your data from Letterboxd by going to `Settings > Import & Export > Export Your Data` and extract the generated zip file.

Then execute script with required options:
```bash
usage: migrate.py [-h] --letterboxd_data LETTERBOXD_DATA --username USERNAME --password PASSWORD --migration {ratings,watchlist}

options:
  -h, --help            show this help message and exit
  --letterboxd_data LETTERBOXD_DATA
                        The path to your exported Letterboxd data. Required.
  --username USERNAME   Your ratehouse username/email. Required.
  --password PASSWORD   Your ratehouse password. Required.
  --migration {ratings,watchlist}
                        The type of migration to run. Required.

```