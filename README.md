# Planet patrol geodata processor 

Adding geospatial data analysis to citizen science data.

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
