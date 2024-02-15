# Planet patrol geodata processor

Adding geospatial data analysis to citizen science data.

## Pre-requisites

The processor is written in Python 3. It uses spatialite and SQLite databases to do the reverse geocoding. The processor is designed to run in a GitHub action, but can be run locally.

Setup (MacOS):

```console
brew install sqlite libspatialite
pip install spatialite requests
```

On MacOS, you may need to add the following to your path to temporarily use the homebrew version of sqlite.

```console
export PATH="$(brew --prefix sqlite)/bin:${PATH}"
export PATH="$(brew --prefix libspatialite)/lib:${PATH}"
export LDFLAGS="-L$(brew --prefix sqlite)/lib"
export CPPFLAGS="-I$(brew --prefix sqlite)/include"
```

Ensure you are using a version of python that supports and allows loading extensions.

Setup (Linux):

```console
apt-get install libsqlite3-mod-spatialite
pip install spatialite requests
```

## What is it?

This project takes the public API data from the Planet Patrol app and adds some geospatial intelligence, using local SQLite and Spatialite databases. It can be used to process the following API endpoints

- `photos.json` for litter uploads
- `incidents.json` for pollution incidents
- `readings.json` for water readings

All of these data sources include a location object for each reading e.g. `{ location: { longitude: -2, latitude: 52.5 }}`. The processor loops through all the entries and uses the longitude and latitude values to do a reverse geocode, using a set of spatialite and SQLite databases. Those databases are taken from the Geovation [postcode-lookup-sqlite](https://github.com/Geovation/postcode-lookup-sqlite) project. This provides a nearest postcode and associated administrative geographies.

The process creates the following files, which can then be ingested by the app as replacements for the original data.

- `photos_geo.json`
- `incidents_geo.json`
- `readings_geo.json`

When existing files are present the processor won't attempt to re-generate the data for those entries that already processed. This should mean that update runs should complete very quickly.

The process runs for dev, test, and prod environments, separated by folders.

## Schedule

The processor uses GitHub actions to schedule running and updating the files. This runs on a nightly basis using the following schedule.

```
cron: '0 0 * * *'
```

This will update the source files, as well as updating the geocode versions.
