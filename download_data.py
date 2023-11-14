import requests

readings_url_prod = "https://api.plasticpatrol.co.uk/readings.json"
readings_url_dev = "https://us-central1-plastic-patrol-dev-722eb.cloudfunctions.net/api/readings.json"
readings_url_test = "https://us-central1-plastic-patrol-dev-test.cloudfunctions.net/api/readings.json"

photos_url_prod = "https://api.plasticpatrol.co.uk/photos.json"
photos_url_dev = "https://us-central1-plastic-patrol-dev-722eb.cloudfunctions.net/api/photos.json"
photos_url_test = "https://us-central1-plastic-patrol-dev-test.cloudfunctions.net/api/photos.json"

incidents_url_prod = "https://api.plasticpatrol.co.uk/incidents.json"
incidents_url_dev = "https://us-central1-plastic-patrol-dev-722eb.cloudfunctions.net/api/incidents.json"
incidents_url_test = "https://us-central1-plastic-patrol-dev-test.cloudfunctions.net/api/incidents.json"

# Download readings, photos, and incidents JSON file and save locally


def saveFileFromUrl(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)


saveFileFromUrl(readings_url_prod, "prod/readings.json")
saveFileFromUrl(photos_url_prod, "prod/photos.json")
saveFileFromUrl(incidents_url_prod, "prod/incidents.json")

saveFileFromUrl(readings_url_dev, "dev/readings.json")
saveFileFromUrl(photos_url_dev, "dev/photos.json")
saveFileFromUrl(incidents_url_dev, "dev/incidents.json")

saveFileFromUrl(readings_url_test, "test/readings.json")
saveFileFromUrl(photos_url_test, "test/photos.json")
saveFileFromUrl(incidents_url_test, "test/incidents.json")
