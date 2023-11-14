import json
import csv
from datetime import datetime

readings_file_prod = "prod/readings"

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
        "name": "pH",
        "displayName": "pH Reading",
        "type": "number"
    }
]


def ConvertEpochSecondsToDateTime(epoch):
    if (epoch == None):
        return ""
    else:
        return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def ConvertEpochMillisecondsToDateTime(epoch):
    if (epoch == None):
        return ""
    else:
        return datetime.fromtimestamp(epoch / 1000.0).strftime('%Y-%m-%d %H:%M:%S')


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


def ConvertFieldNamesToDisplayNames(csv_data):
    new_csv_data = []
    for i in csv_data:
        row = {}
        for k in reading_fields:
            field_value = ""
            for j in i.keys():
                if (j == k['name']):
                    if (k['type'] == 'datetime_seconds'):
                        field_value = ConvertEpochSecondsToDateTime(i[j])
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
    # sort by dateTime field
    # the dateTime field could be None
    json_data.sort(key=lambda x: x['dateTime'] if x['dateTime'] else 0)
    for i in json_data:
        rows.append(FlattenJsonObj(i))
    return rows


def LoadJsonFile(filename):
    file_data = json.load(open(filename))
    return file_data


def ProcessFileToCSV(filename, type):
    json_data = LoadJsonFile(filename + '_geo.json')
    csv_data = ConvertJSONToCSVData(json_data, type)
    csv_display_data = ConvertFieldNamesToDisplayNames(csv_data)

    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_display_data[0].keys())
        writer.writeheader()
        for data in csv_display_data:
            writer.writerow(data)


ProcessFileToCSV(readings_file_prod, 'readings')
