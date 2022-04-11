import pandas as pd
from flask import Flask, request, send_from_directory, render_template_string, Response
import json
import process
import process_stations

app = Flask(__name__)
stations_reader = process_stations.StationsReader('stations.csv')
tide_reader = process.Reader('tideReadings.csv')


def is_in_stations_name(stationName):
    return stationName in stations_reader.data.stationName.values


def is_in_stations_ref(stationReference):
    return stationReference in stations_reader.data.stationReference.values


# This is a stub showing the beginnings of one required endpoint
# Must be editted to match API.rst description.

@app.route('/station/json')
def station_info():
    stationName = request.args.get('stationName', default=None, type=str)
    stationReference = request.args.get('stationReference', default=None, type=str)
    # Search by name
    if stationName is not None and stationReference is None:
        if " " in stationName:
            stationName = stationName.replace(" ", "+")
            if not is_in_stations_name(stationName):
                return f'The station name you input is wrong!'
            else:
                name_json = {
                    'stationName': stationName,
                    'stationReference': stations_reader.get_reference(stationName),
                    "northing": stations_reader.get_northing(stations_reader.searchByname(stationName)),
                    "easting": stations_reader.get_easting(stations_reader.searchByname(stationName)),
                    "latitude": stations_reader.get_latitude(stations_reader.searchByname(stationName)),
                    "longitude": stations_reader.get_longitude(stations_reader.searchByname(stationName))
                }
                return json.dumps(name_json)
    elif stationName is None and stationReference is not None:
        if not is_in_stations_ref(stationReference):
            return f'The station you input is wrong!'
        else:
            reference_json = {
                'stationName': stations_reader.get_name(stationReference),
                'stationReference': stationReference,
                "northing": stations_reader.get_northing(stations_reader.searchByreference(stationReference)),
                "easting": stations_reader.get_easting(stations_reader.searchByreference(stationReference)),
                "latitude": stations_reader.get_latitude(stations_reader.searchByreference(stationReference)),
                "longitude": stations_reader.get_longitude(stations_reader.searchByreference(stationReference))
            }
            return json.dumps(reference_json)
    elif stationName is None and stationReference is None:
        return f"Please input the station name or the station reference!"
    else:
        return f"You can only input the station name or the station reference!"


# This is an example of a quick way to send a file.
# There is plenty of room for improvement.
@app.route('/data/graph')
def data_graph():
    """Return a graph of station data.

    The endpoint accepts query parameters:
    * stationName
    * stationRef
    * from
    * to
    """
    stationName = request.args.get('stationName', default=None, type=str)
    stationReference = request.args.get('stationReference', default=None, type=str)
    t_from = request.args.get('t_from', default=None, type=str)
    t_to = request.args.get('t_to', default=None, type=str)
    t_from, t_to = set_time_range(t_from, t_to)
    if stationName is not None and stationReference is None:
        if " " in stationName:
            stationName = stationName.replace(" ", "+")
        if not is_in_stations_name(stationName):
            return f'The station you input is wrong!'
        else:
            tide_reader.station_graph([stationName], time_from=t_from, time_to=t_to)
            return send_from_directory(".", stationName + ".png")
    elif stationName is None and stationReference is not None:
        if not is_in_stations_ref(stationReference):
            return f'The station you input is wrong!'
        else:
            station_name = stations_reader.get_name(stationReference)
            tide_reader.station_graph([station_name], time_from=t_from, time_to=t_to)
            return send_from_directory(".", station_name + ".png")
    elif stationName is None and stationReference is None:
        return f"Please input the station name or the station reference!"
    else:
        return f"You can only input the station name or the station reference!"


def set_time_range(t_from, t_to):
    if t_from is None and t_to is not None:
        t_from = '2021-09-20T00:00:00Z'
        return t_from, t_to
    elif t_from is not None and t_to is None:
        t_to = '2021-09-26T06:00:00Z'
        return t_from, t_to
    elif t_from is None and t_to is None:
        t_from = '2021-09-20T00:00:00Z'
        t_to = '2021-09-26T06:00:00Z'
        return t_from, t_to
    else:
        return t_from, t_to


@app.route('/data/json/write', methods=['POST', 'GET'])
def write2csv():
    if request.method == 'GET':
        tide_reader.add_data(request.form.get('dateTime'), request.form.get('stationName'),
                             request.form.get('tideValue'))
        tide_reader.write_data("new.csv")
        write_json = {
            "stationName": request.form.get('stationName'),
            "dateTime": request.form.get('dateTime'),
            "tideValue": request.form.get('tideValue')
        }
        return json.dumps(write_json)
    else:
        return f'Write Nothing!'


@app.route('/data/json', methods=['GET', 'POST'])
def tide_info():
    # tideReader = process.Reader('tideReadings.csv')
    stationName = request.args.get('stationName', default=None, type=str)
    stationReference = request.args.get('stationReference', default=None, type=str)
    t_from = request.args.get('t_from', default=None, type=str)
    t_to = request.args.get('t_to', default=None, type=str)
    statistic = request.args.get('statistic', default=None, type=str)
    t_from, t_to = set_time_range(t_from, t_to)
    if request.method == 'GET':
        if " " in stationName:
            stationName = stationName.replace(" ", "+")
        if is_in_stations_name(stationName) or is_in_stations_ref(stationReference):
            if stationName is not None and stationReference is None:
                name_json = tide_info_statistic(stationName, t_from, t_to, statistic)
                return name_json
            elif stationName is None and stationReference is not None:
                stationName = stations_reader.get_name(stationReference)
                ref_json = tide_info_statistic(stationName, t_from, t_to, statistic)
                return ref_json
            elif stationName is None and stationReference is None:
                return f"Please input the station name or the station reference!"
            else:
                return f"You can only input the station name or the station reference!"
        else:
            return f'The station you input is wrong!'
    elif request.method == 'POST':
        write_file = request.args.get('write')
        json_data = json.loads(str(request.get_data(), encoding='utf-8'))
        if write_file == 'True':
            for row in range(len(json_data)):
                station_name = json_data[row]["stationName"]
                date_time = json_data[row]["dateTime"]
                tide_value = json_data[row]["tideValue"]
                tide_reader.add_data(date_time, station_name, tide_value)
                # print(tide_reader.data)
                tide_reader.write_data("tideReadings.csv")
        return "json_data"


@app.route('/data/html', methods=['GET', 'POST'])
def data_html():
    stationName = request.args.get('stationName', default=None, type=str)
    stationReference = request.args.get('stationReference', default=None, type=str)
    t_from = request.args.get('t_from', default=None, type=str)
    t_to = request.args.get('t_to', default=None, type=str)
    statistic = request.args.get('statistic', default=None, type=str)
    t_from, t_to = set_time_range(t_from, t_to)
    if request.method == 'GET':
        if is_in_stations_name(stationName) or is_in_stations_ref(stationReference):
            if stationName is not None and stationReference is None:
                name_json = tide_info_statistic(stationName, t_from, t_to, statistic)
                # TABLE = pd.DataFrame(name_json["stationName"], name_json["tideValue"])
                TABLE = pd.DataFrame(tide_reader.station_tides(stationName, t_from, t_to))
                return TABLE.to_html()
            elif stationName is None and stationReference is not None:
                stationName = stations_reader.get_name(stationReference)
                ref_json = tide_info_statistic(stationName, t_from, t_to, statistic)
                TABLE = pd.DataFrame(ref_json["stationName"], ref_json["dateTime"], ref_json["tideValue"])
                return TABLE.to_html()
            elif stationName is None and stationReference is None:
                return f"Please input the station name or the station reference!"
            else:
                return f"You can only input the station name or the station reference!"
        else:
            return f'The station you input is wrong!'


def tide_info_statistic(stationName, time_from, time_to, statistic):
    if is_in_stations_name(stationName):
        if statistic is None:
            value_json = {
                "stationName": stationName,
                "stationReference": stations_reader.get_reference(stationName),
                "from": time_from,
                "to": time_to,
                "tideValues": tide_reader.station_tides([stationName], time_from, time_to)[stationName].to_dict()
            }
            return value_json
        elif statistic == 'max':
            max = tide_reader.max_tides(time_from, time_to)[stationName]
            max_json = {
                "stationName": stationName,
                "stationReference": stations_reader.get_reference(stationName),
                "from": time_from,
                "to": time_to,
                "max": max
            }
            return max_json
        elif statistic == 'min':
            min = tide_reader.min_tides(time_from, time_to)[stationName]
            min_json = {
                "stationName": stationName,
                "stationReference": stations_reader.get_reference(stationName),
                "from": time_from,
                "to": time_to,
                "min": min
            }
            return min_json
        elif statistic == 'mean':
            mean = tide_reader.mean_tides(time_from, time_to)[stationName]
            mean_json = {
                "stationName": stationName,
                "stationReference": stations_reader.get_reference(stationName),
                "from": time_from,
                "to": time_to,
                "mean": mean
            }
            return mean_json
    else:
        return f'The station you input is wrong!'


if __name__ == '__main__':
    app.run()
