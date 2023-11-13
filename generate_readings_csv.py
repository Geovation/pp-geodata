import json
import csv
from datetime import datetime

readings_file_prod = "prod/readings"


def ConvertEpochToDateTime(epoch):
    return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def FlattenJsonObj(json):
    val = {}
    for i in json.keys():
        if isinstance(json[i], dict):
            get = FlattenJsonObj(json[i])
            for j in get.keys():
                if (j == 'dateTime'):
                    val[j] = ConvertEpochToDateTime(get[j])
                else:
                    val[j] = get[j]
        else:
            if (i == 'dateTime'):
                val[i] = ConvertEpochToDateTime(json[i])
            else:
                val[i] = json[i]
    return val


def ConvertJSONToCSVData(json, type):
    rows = []
    for i in json[type]:
        rows.append(FlattenJsonObj(i))
    return rows


def LoadJsonFile(filename):
    file_data = json.load(open(filename))
    return file_data


def ProcessFileToCSV(filename, type):
    json_data = LoadJsonFile(filename + '_geo.json')
    csv_data = ConvertJSONToCSVData(json_data, type)

    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_data[0].keys())
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)


ProcessFileToCSV(readings_file_prod, 'readings')
