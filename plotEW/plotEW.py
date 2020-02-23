from typing import List

import matplotlib.pyplot as plt

from obspy import UTCDateTime, Stream, Trace
from obspy.clients.earthworm import Client


def init_client(server: str, port: int, **kwargs):
    """
    Initialize an earthworm client on the given server and port
    :param server: IP address for the machine running earthworm wave server
    :type server: int
    :param port: Port for the earthworm wave server
    :type port: int
    :param **kwargs: Additional kwargs passed to obspy's Client call
    :return: Obspy Client object
    :rtype: Client
    """
    client = Client(server, port, **kwargs)
    return client


def read_station_file(filename: str) -> List[str]:
    """
    Read a text file of stations named by SEED format
    (Net.Station.Location.Channel). One station per line.
    :param filename: filename of station file
    :type filename: str
    :return: List of station name strings
    :rtype: List<str>
    """
    with open(filename, 'r') as f:
        data = f.read().split('\n')

    stas = [d for d in data if d]
    return stas


def get_waveforms(client: Client, seed_id: str, starttime: UTCDateTime,
                  endtime: UTCDateTime) -> Stream:
    """
    Retrieve waveforms from earthworm wave server specified by client.
    :param client: Instance of Obspy's Client
    :type client: Client
    :param seed_id: Station name formatted to follow SEED format
    :type seed_id: str
    :param starttime: Start time for data request
    :type starttime: UTCDateTime
    :param endtime: End time for data request
    :type endtime: UTCDateTime
    :return: Obspy stream containing the waveform(s)
    :rtype: Stream
    """
    net, sta, loc, chan = seed_id.split('.')
    st = client.get_waveforms(net, sta, loc, chan, starttime, endtime)
    return st


def plot_helicorder(tr: Trace, outfile: str = None, **kwargs) -> plt.Axes:
    """
    Plot a helicorder style plot.  1 channel for a day of data.  Defaults to
    showing 60 minutes of data per line in the helicorder.
    :param st: Obspy Trace object of data to plot
    :type st: Stream
    :param **kwargs: Valid Stream.plot(type='dayplot') parameters
    :return: ax containing plot
    :rtype: plt.Axes
    """
    ax = tr.plot(type='dayplot', interval=60, show_y_UTC_label=False,
                 outfile=outfile, **kwargs)
    return ax


def plot_stream(st: Stream, outfile: str = None, **kwargs) -> plt.Axes:
    """
    Plot obspy stream (see obspy stream method).
    :param st: Obpsy stream containing data to plot
    :type st: Stream
    :param outfile: filename to save file to.  Format is determined from
        file extension
    :type outfile: str
    :return: ax containing plot
    :rtype: plt.Axes
    """
    st.plot(outfile=outfile, **kwargs)


def basic_processing(st: Stream, remove_trend: bool = True,
                     remove_mean: bool = True, filter_type: str = None,
                     **kwargs) -> None:
    """
    Process an obspy stream using frequent methods. Can remove the mean,
    remove the trend, and filter the data.
    :param st: Obspy Stream containing data to process
    :type st: Stream
    :param remove_trend: Remove the trend in the data using simple linear
        method
    :type remove_trend: bool
    :param remove_mean: Remove the mean in the data
    :type remove_mean: bool
    :param filter_type: Filter the data using specified obspy filter
    :type filter_type: str
    :param **kwargs: Values to pass to obspy stream.filter method
    :return: None..Stream is modified in place and the original data is no
        longer accessible after
    :rtype: None
    """
    if remove_mean:
        st.detrend('demean')

    if remove_trend:
        st.detrend('linear')

    if filter_type:
        st.filter(filter_type, **kwargs)
