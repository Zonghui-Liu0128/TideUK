""" Module containing a class to process tidal data."""

import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Reader:
    """
    Class to process tidal data.

    data : pandas.DataFrame
        The underlying tide data.
    """

    def __init__(self, filename):
        """Read in the rainfall data from a named ``.csv``
           file using ``pandas``.

        The DataFrame data is stored in a class instance variable ``data``
        indexed by entry.

        Parameters
        ----------

        filename: str
            The file to be read

        Examples
        --------

        # >>> Reader("tidalReadings.csv").data.loc[0].stationName
        'Bangor'
        """
        self.data = pd.read_csv(filename)

    def station_tides(self, station_name, time_from=None, time_to=None):
        """Return the tide data at a named station as an ordered pandas Series,
         indexed by the dateTime data.

        Parameters
        ----------

        station_name: str or list of strs
            Station Name(s) to return
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.DataFrame
            The relevant tide data indexed by dateTime and with columns the stationName(s)

        Examples
        --------

        # >>> reader = Reader("tideReadings.csv")
        # >>> tides = reader.station_tides(["Newlyn", "Bangor"])
        # >>> tides.loc["2021-09-20T02:00:00Z", "Newlyn"]
        0.937

        """
        # Filter the records of given stations
        tide_station_row = self.data.loc[self.data.stationName.isin(station_name)]
        noise_mean_tides = tide_station_row[pd.to_numeric(tide_station_row['tideValue'], errors='coerce').notnull()]
        # Slice the records based on dateTime range
        if time_from is None and time_to is not None:
            tide_station_sliced = noise_mean_tides.loc[noise_mean_tides.dateTime <= time_to]
        elif time_from is not None and time_to is None:
            tide_station_sliced = noise_mean_tides.loc[noise_mean_tides.dateTime >= time_from]
        elif time_from is None and time_to is None:
            tide_station_sliced = noise_mean_tides
        else:
            tide_station_sliced = noise_mean_tides.loc[
                (noise_mean_tides.dateTime >= time_from) & (noise_mean_tides.dateTime <= time_to)]
        # Modify the dataframe's index and columns
        tide_station_tmp = tide_station_sliced.astype({'tideValue': float}).set_index(['dateTime', 'stationName'])[
            'tideValue']
        tide_station_res = tide_station_tmp.unstack()
        return tide_station_res

    def max_tides(self, time_from=None, time_to=None):
        """Return the high tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format).
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        # >>> reader = Reader("tideReadings.csv")
        # >>> tides = reader.max_tides()
        # >>> tides["Newlyn"]
        2.376
        """
        # Slice dataframe based on time range
        station_max_row = self.data.loc[(self.data.dateTime >= time_from) & (self.data.dateTime <= time_to)]
        # Remove the noise
        noise_max_tides = station_max_row[pd.to_numeric(station_max_row['tideValue'], errors='coerce').notnull()]
        # Get every station's max tide value(without noise)
        max_tides_float = noise_max_tides.astype({'tideValue': float})
        res_max_tides = max_tides_float.sort_values('tideValue', ascending=False).groupby('stationName',
                                                                                          as_index=True).first()

        return res_max_tides["tideValue"]

    def min_tides(self, time_from=None, time_to=None):
        """Return the low tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        # >>> reader = Reader("tideReadings.csv")
        # >>> tides = reader.min_tides()
        # >>> tides["Newlyn"]
        # -2.231
        """
        # Slice dataframe based on time range
        station_min_row = self.data.loc[(self.data.dateTime >= time_from) & (self.data.dateTime <= time_to)]
        # Remove the noise
        noise_min_tides = station_min_row[pd.to_numeric(station_min_row['tideValue'], errors='coerce').notnull()]
        # Get every station's min tide value(without noise)
        min_tides_float = noise_min_tides.astype({'tideValue': float})
        res_min_tides = min_tides_float.sort_values('tideValue', ascending=True).groupby('stationName',
                                                                                         as_index=True).first()
        return res_min_tides['tideValue']

    def mean_tides(self, time_from=None, time_to=None):
        """Return the mean tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        # >>> reader = Reader("tideReadings.csv")
        # >>> tides = reader.mean_tides()
        # >>> tides["Newlyn"]
        # 0.19242285714285723
        """
        station_mean_row = self.data.loc[(self.data.dateTime >= time_from) & (self.data.dateTime <= time_to)]
        # Remove the noise
        noise_mean_tides = station_mean_row[pd.to_numeric(station_mean_row['tideValue'], errors='coerce').notnull()]
        mean_tides_float = noise_mean_tides.astype({'tideValue': float})
        res_mean_tides = mean_tides_float.groupby('stationName').tideValue.mean()
        return res_mean_tides

    def station_graph(self, station_name, time_from=None, time_to=None):
        """Return a matplotlib graph of the tide data at a named station,
        indexed by the dateTime data.

        Parameters
        ----------

        station_name: str
            Station Name
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        matplotlib.figure.Figure
            Labelled graph of station tide data.
        """
        res_df = self.station_tides(station_name, time_from, time_to)
        # print(res_df)
        res_df_float = res_df.astype('float64')
        plot = res_df_float.plot()
        plt.show()
        fig = plot.get_figure()
        fig.savefig(station_name[0] + '.png')

    def add_data(self, date_time, station_name, tide_value):
        """Add data to the reader DataFrame.

        Parameters
        ----------
        date_time: str
            Time of reading in ISO 8601 format
        station_name: str
            Station Name
        time_value: float
            Observed tide in m

        Examples
        --------

        # >>> reader = Reader("tideReadings.csv")
        # >>> original_len = len(reader.data.index)
        # >>> reader.add_data("2021-09-20T02:00:00Z",
        #                     "Newlyn", 1.465)
        # >>> len(reader.data.index) = original_len + 1
        # True
        """
        row_data = self.data
        len_row = len(row_data)
        # Generate a new dictionary to generate a new dataframe later
        new_dic = {'dateTime': date_time, 'stationName': station_name, 'tideValue': tide_value}
        # Generate a new dataframe using dictionary and set the index
        new_dataframe = pd.DataFrame(data=new_dic, index=[len(row_data)])
        # Append the new dataframe to the original dataframe
        self.data = row_data.append(new_dataframe)
        # Judge right or not
        len_new = len(self.data)
        # print(self.data)
        if len_new == len_row + 1:
            return True
        else:
            return False

    def write_data(self, filename):
        """Write data to disk in .csv format.

        Parameters
        ----------

        filename: str
            filename to write to.
        """
        tides = self.data[pd.to_numeric(self.data['tideValue'], errors='coerce').notnull()]
        tmp = tides.to_csv(filename, index=False)
        if tmp:
            return False
        else:
            return True


if __name__ == "__main__":
    reader = Reader("tideReadings.csv")
    '''Test for the init function'''
    # print(reader.data)
    '''Test for the station_tides() function'''
    res_station_tides = reader.station_tides(["St+Marys"], '2021-09-20T00:00:00Z', '2021-09-26T06:00:00Z')
    print(res_station_tides)
    # print(res_station_tides.loc["2021-09-20T02:00:00Z", "Newlyn"])
    '''Test for the max_tides() function'''
    # res_max_tides = reader.max_tides('2021-09-20T00:00:00Z', '2021-09-26T06:00:00Z')
    # print(res_max_tides)
    # print(res_max_tides["Newlyn"])
    '''Test for the min_tides() function'''
    # res_min_tides = reader.min_tides('2021-09-20T00:00:00Z', '2021-09-26T06:00:00Z')
    # print(res_min_tides)
    # print(res_min_tides["Newlyn"])
    '''Test for the mean_tides() function'''
    # res_mean_tides = reader.mean_tides('2021-09-20T00:00:00Z', '2021-09-26T06:00:00Z')
    # print(res_mean_tides)
    # print(res_mean_tides["Newlyn"])
    '''Test for add_data() function'''
    # res_add_data = reader.add_data("2021-09-27T00:00:00Z", "Newlyn", 1.465)
    # print(res_add_data)
    '''Test for the write_data() function'''
    # res_write_data = reader.write_data('/Users/lzh/Desktop/mpm-assessment-2-acse-3abf3f9d/test_write.csv')
    # print(res_write_data)
    '''Test for the station_graph() function'''
    # reader.station_graph(['Newlyn'], '2021-09-20T00:00:00Z', '2021-09-25T06:00:00Z')
    # reader.station_graph(["Newlyn", "Bangor"], '2021-09-20T00:00:00Z', '2021-09-25T06:00:00Z')

    # try:
    #     print(len(reader.data.index))
    # except TypeError:
    #     print("No data loaded.")
