import json
import os
import spatialite

regions_geo_db = "geocoder/regions_geo.sqlite"
postcode_lookup_db = "geocoder/postcodes.sqlite"
postcode_geo_db_east_midlands = "geocoder/postcodes_geo_east_midlands.sqlite"
postcode_geo_db_east_of_england = "geocoder/postcodes_geo_east_of_england.sqlite"
postcode_geo_db_london = "geocoder/postcodes_geo_london.sqlite"
postcode_geo_db_north_east = "geocoder/postcodes_geo_north_east.sqlite"
postcode_geo_db_north_west = "geocoder/postcodes_geo_north_west.sqlite"
postcode_geo_db_south_east = "geocoder/postcodes_geo_south_east.sqlite"
postcode_geo_db_south_west = "geocoder/postcodes_geo_south_west.sqlite"
postcode_geo_db_west_midlands = "geocoder/postcodes_geo_west_midlands.sqlite"
postcode_geo_db_yorkshire_and_the_humber = "geocoder/postcodes_geo_yorkshire_and_the_humber.sqlite"
postcode_geo_db_wales = "geocoder/postcodes_geo_wales.sqlite"
postcode_geo_db_scotland = "geocoder/postcodes_geo_scotland.sqlite"

readings_file_prod = "prod/readings"
readings_file_dev = "dev/readings"
readings_file_test = "test/readings"

photos_file_prod = "prod/photos"
photos_file_dev = "dev/photos"
photos_file_test = "test/photos"

incidents_file_prod = "prod/incidents"
incidents_file_dev = "dev/incidents"
incidents_file_test = "test/incidents"

readings_files = [readings_file_prod, readings_file_dev, readings_file_test]
photos_files = [photos_file_prod, photos_file_dev, photos_file_test]
incidents_files = [incidents_file_prod,
                   incidents_file_dev, incidents_file_test]


def LoadJsonFile(filename):
    file_data = json.load(open(filename, 'r', encoding='utf-8'))
    return file_data


def GetGeocodeData(longitude, latitude):
    with spatialite.connect(regions_geo_db) as region_db, spatialite.connect(postcode_lookup_db) as postcode_lookup, spatialite.connect(postcode_geo_db_east_midlands) as postcode_db_east_midlands, spatialite.connect(postcode_geo_db_east_of_england) as postcode_db_east_of_england, spatialite.connect(postcode_geo_db_london) as postcode_db_london, spatialite.connect(postcode_geo_db_north_east) as postcode_db_north_east, spatialite.connect(postcode_geo_db_north_west) as postcode_db_north_west, spatialite.connect(postcode_geo_db_south_east) as postcode_db_south_east, spatialite.connect(postcode_geo_db_south_west) as postcode_db_south_west, spatialite.connect(postcode_geo_db_west_midlands) as postcode_db_west_midlands, spatialite.connect(postcode_geo_db_yorkshire_and_the_humber) as postcode_db_yorkshire_and_the_humber, spatialite.connect(postcode_geo_db_wales) as postcode_db_wales, spatialite.connect(postcode_geo_db_scotland) as postcode_db_scotland:

        region_postcodes_dbs = {
            'east_midlands': postcode_db_east_midlands,
            'east_of_england': postcode_db_east_of_england,
            'london': postcode_db_london,
            'north_east': postcode_db_north_east,
            'north_west': postcode_db_north_west,
            'south_east': postcode_db_south_east,
            'south_west': postcode_db_south_west,
            'west_midlands': postcode_db_west_midlands,
            'yorkshire_and_the_humber': postcode_db_yorkshire_and_the_humber,
            'wales': postcode_db_wales,
            'scotland': postcode_db_scotland
        }

        region_result = region_db.execute('select code, name from regions where within(makepoint(?, ?, 4326), geom)', [
            float(longitude), float(latitude)]).fetchone()
        if region_result is None:
            return None
        else:
            region_name_lower = region_result[1].replace(' ', '_').lower()

            if region_name_lower not in region_postcodes_dbs:
                return None

            regional_db = region_postcodes_dbs[region_name_lower]
            regional_db.execute('select * from postcodes limit 1')

            postcode_result = regional_db.execute('select postcode from postcodes order by distance(makepoint(?, ?, 4326), geom) limit 1', [
                float(longitude), float(latitude)]).fetchone()
            if postcode_result is None:
                return None
            else:
                postcode_info = postcode_lookup.execute(
                    'select * from vw_postcodes where postcode = ?', [postcode_result[0]]).fetchone()
                if postcode_info is None:
                    return None
                else:
                    return {
                        'region': region_result[1],
                        'postcode': postcode_info[0],
                        'district': postcode_info[3],
                        'country': postcode_info[5]
                    }


def ProcessGeocodeDataForFile(filename, type):
    file_data = LoadJsonFile(filename + '.json')

    already_processed_data_dict = {}
    processed_file_exists = os.path.isfile(filename + '_geo.json')

    print('Processing ' + filename + '...')

    if processed_file_exists:
        already_processed_data = LoadJsonFile(filename + '_geo.json')
        data_array = already_processed_data[type]
        # key already processed data by id
        for reading in data_array:
            if (type == 'photos'):
                reading_id = reading
                reading = data_array[reading]
            else:
                reading_id = reading['id']
            already_processed_data_dict[reading_id] = reading

    data_array = file_data[type]

    for reading in data_array:
        if (type == 'photos'):
            reading_id = reading
            reading = data_array[reading]
            reading['id'] = reading_id

        if (type == 'photos'):
            longitude = reading['location']['_longitude']
            latitude = reading['location']['_latitude']
        else:
            longitude = reading['location']['longitude']
            latitude = reading['location']['latitude']

        # If we've already done it, get the data from the already processed file
        if processed_file_exists and reading['id'] in already_processed_data_dict and 'geodata' in already_processed_data_dict[reading['id']]:
            reading['geodata'] = already_processed_data_dict[reading['id']]['geodata']
        elif longitude is not None and latitude is not None:
            geocode_data = GetGeocodeData(longitude, latitude)
            if geocode_data is not None:
                reading['geodata'] = geocode_data

    with open(filename + '_geo.json', 'w', encoding='utf-8') as outfile:
        json.dump(file_data, outfile)


ProcessGeocodeDataForFile(readings_file_prod, 'readings')
ProcessGeocodeDataForFile(readings_file_dev, 'readings')
ProcessGeocodeDataForFile(readings_file_test, 'readings')

ProcessGeocodeDataForFile(photos_file_prod, 'photos')
ProcessGeocodeDataForFile(photos_file_dev, 'photos')

ProcessGeocodeDataForFile(incidents_file_prod, 'incidents')
ProcessGeocodeDataForFile(incidents_file_dev, 'incidents')
ProcessGeocodeDataForFile(incidents_file_test, 'incidents')
