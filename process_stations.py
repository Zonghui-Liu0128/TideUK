import pandas as pd
import requests


class StationsReader():
    def __init__(self, filename):
        self.url = ''
        self.data = pd.read_csv(filename)

    def searchByname(self, station_name):
        df = self.data
        if station_name in self.data.stationName.values:
            res_search_name = df.loc[df['stationName'] == station_name, 'stationURL']
            url = list(res_search_name)[0]
            return url
        else:
            return "wrong"

    def searchByreference(self, station_reference):
        df = self.data
        if station_reference in self.data.stationReference.values:
            res_search_reference = df.loc[df['stationReference'] == station_reference, 'stationURL']
            url = list(res_search_reference)[0]
            return url
        else:
            return "wrong"

    def get_northing(self, url):
        r = requests.get(url)
        data_json = r.json()
        return data_json['items']['northing']

    def get_easting(self, url):
        r = requests.get(url)
        data_json = r.json()
        return data_json['items']['easting']

    def get_latitude(self, url):
        r = requests.get(url)
        data_json = r.json()
        return data_json['items']['lat']

    def get_longitude(self, url):
        r = requests.get(url)
        data_json = r.json()
        return data_json['items']['long']

    def get_reference(self, station_name):
        df = self.data
        if station_name in self.data.stationName.values:
            res_get_ref = df.loc[df['stationName'] == station_name, 'stationReference']
            return list(res_get_ref)[0]
        else:
            return ""

    def get_name(self, station_reference):
        df = self.data
        if station_reference in self.data.stationReference.values:
            res_get_name = df.loc[df['stationReference'] == station_reference, 'stationName']
            return list(res_get_name)[0]
        else:
            return "wrong"



if __name__ == '__main__':
    stations_reader = StationsReader('stations.csv')
    # print(stations_reader.data)
    # print(stations_reader.searchByname('Bangor'))
    # print(stations_reader.searchByreference('E73839'))
    # print(stations_reader.get_northing())
