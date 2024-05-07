import json
import csv
import datetime

readings_file_prod = "prod/readings"
readings_file_dev = "dev/readings"
readings_file_test = "test/readings"

incidents_file_prod = "prod/incidents"
incidents_file_dev = "dev/incidents"
incidents_file_test = "test/incidents"

photos_file_prod = "prod/photos"
photos_file_dev = "dev/photos"
photos_file_test = "test/photos"

reading_fields = [
    {
        "name": "id",
        "displayName": "ID",
        "type": "string"
    },
    {
        "name": "userId",
        "displayName": "User ID",
        "type": "string"
    },
    {
        "name": "readingType",
        "displayName": "Reading Type",
        "type": "string"
    },
    {
        "name": "dateTime",
        "displayName": "Date",
        "type": "datetime_milliseconds"
    },
    {
        "name": "waterwayName",
        "displayName": "Waterway Name",
        "type": "string"
    },
    {
        "name": "testKitName",
        "displayName": "Test Kit Name",
        "type": "string"
    },
    {
        "name": "latitude",
        "displayName": "Latitude",
        "type": "number"
    },
    {
        "name": "longitude",
        "displayName": "Longitude",
        "type": "number"
    },
    {
        "name": "region",
        "displayName": "Region",
        "type": "string"
    },
    {
        "name": "postcode",
        "displayName": "Postcode",
        "type": "string"
    },
    {
        "name": "district",
        "displayName": "District",
        "type": "string"
    },
    {
        "name": "country",
        "displayName": "Country",
        "type": "string"
    },
    {
        "name": "coliforms",
        "displayName": "Coliforms Reading",
        "type": "boolean"
    },
    {
        "name": "phosphateReading",
        "displayName": "Phosphate Reading",
        "type": "number"
    },
    {
        "name": "phosphateUnits",
        "displayName": "Phosphate Units",
        "type": "string"
    },
    {
        "name": "nitriteReading",
        "displayName": "Nitrite Reading",
        "type": "number"
    },
    {
        "name": "nitriteUnits",
        "displayName": "Nitrite Units",
        "type": "string"
    },
    {
        "name": "nitrateReading",
        "displayName": "Nitrate Reading",
        "type": "number"
    },
    {
        "name": "nitrateUnits",
        "displayName": "Nitrate Units",
        "type": "string"
    },
    {
        "name": "ph",
        "displayName": "pH Reading",
        "type": "number"
    }
]

incident_fields = [
    {
        "name": "id",
        "displayName": "ID",
        "type": "string"
    },
    {
        "name": "userId",
        "displayName": "User ID",
        "type": "string"
    },
    {
        "name": "dateTime",
        "displayName": "Date",
        "type": "datetime_milliseconds"
    },
    {
        "name": "waterwayName",
        "displayName": "Waterway Name",
        "type": "string"
    },
    {
        "name": "description",
        "displayName": "Description",
        "type": "string"
    },
    {
        "name": "latitude",
        "displayName": "Latitude",
        "type": "number"
    },
    {
        "name": "longitude",
        "displayName": "Longitude",
        "type": "number"
    },
    {
        "name": "region",
        "displayName": "Region",
        "type": "string"
    },
    {
        "name": "postcode",
        "displayName": "Postcode",
        "type": "string"
    },
    {
        "name": "district",
        "displayName": "District",
        "type": "string"
    },
    {
        "name": "country",
        "displayName": "Country",
        "type": "string"
    }
]

photo_fields = [
    {
        "name": "id",
        "displayName": "ID",
        "type": "string"
    },
    {
        "name": "created",
        "displayName": "Date",
        "type": "string"
    },
    {
        "name": "pieces",
        "displayName": "Pieces",
        "type": "number"
    },
    {
        "name": "region",
        "displayName": "Region",
        "type": "string"
    },
    {
        "name": "postcode",
        "displayName": "Postcode",
        "type": "string"
    },
    {
        "name": "district",
        "displayName": "District",
        "type": "string"
    },
    {
        "name": "country",
        "displayName": "Country",
        "type": "string"
    }
]


def ConvertEpochToDateTime(epoch):
    if (epoch == None):
        return ""
    else:
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def ConvertEpochMillisecondsToDateTime(epoch):
    if (epoch is None or not isinstance(epoch, int)):
        return ""
    else:
        return ConvertEpochToDateTime(epoch / 1000)


def FlattenJsonObj(json):
    val = {}
    for i in json.keys():
        if isinstance(json[i], dict):
            get = FlattenJsonObj(json[i])
            for j in get.keys():
                val[j] = get[j]
        else:
            val[i] = json[i]
    return val


def ConvertFieldNamesToDisplayNames(csv_data, fields):
    new_csv_data = []
    for i in csv_data:
        row = {}
        for k in fields:
            field_value = ""
            for j in i.keys():
                if (j == k['name']):
                    if (k['type'] == 'datetime_seconds'):
                        field_value = ConvertEpochToDateTime(i[j])
                    elif (k['type'] == 'datetime_milliseconds'):
                        field_value = ConvertEpochMillisecondsToDateTime(i[j])
                    elif (k['type'] == 'string'):
                        field_value = i[j].strip()
                    else:
                        field_value = i[j]

            row[k['displayName']] = field_value
        new_csv_data.append(row)
    return new_csv_data


def ConvertJSONToCSVData(json, type):
    rows = []
    json_data = json[type]

    # If the type is photos then it is keyed by id. convert to a list
    if type == 'photos':
        json_data = []
        for key in json['photos'].keys():
            json_data.append(json['photos'][key])
            json_data.sort(key=lambda x: x['created']
                           if 'created' in x else '')
    else:
        json_data.sort(key=lambda x: x['dateTime'] if x['dateTime'] else 0)
    for i in json_data:
        rows.append(FlattenJsonObj(i))
    return rows


def ProcessFileToCSV(filename, type, fields):
    json_data = LoadJsonFile(filename + '_geo.json')
    csv_data = ConvertJSONToCSVData(json_data, type)
    csv_display_data = ConvertFieldNamesToDisplayNames(csv_data, fields)

    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_display_data[0].keys())
        writer.writeheader()
        for data in csv_display_data:
            writer.writerow(data)


def LoadJsonFile(filename):
    file_data = json.load(open(filename))
    return file_data


ProcessFileToCSV(readings_file_prod, 'readings', reading_fields)
ProcessFileToCSV(readings_file_dev, 'readings', reading_fields)
ProcessFileToCSV(readings_file_test, 'readings', reading_fields)

ProcessFileToCSV(incidents_file_prod, 'incidents', incident_fields)
ProcessFileToCSV(incidents_file_dev, 'incidents', incident_fields)
ProcessFileToCSV(incidents_file_test, 'incidents', incident_fields)

ProcessFileToCSV(photos_file_prod, 'photos', photo_fields)
ProcessFileToCSV(photos_file_dev, 'photos', photo_fields)
