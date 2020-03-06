from typing import List, Union

import matplotlib.pyplot as plt

from obspy import UTCDateTime, Stream, Trace, Inventory, read_inventory
from obspy.clients.earthworm import Client
from obspy.clients.fdsn import Client as IRIS_Client


def init_client(server: str, port: int, from_iris: bool = False, **kwargs):
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
    if from_iris:
        client = IRIS_Client('IRIS')
    else:
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
    fig = tr.plot(type='dayplot', interval=60, show_y_UTC_label=False,
                  outfile=outfile, **kwargs)
    return fig


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
    fig = st.plot(outfile=outfile, **kwargs)
    return fig


def filter(st: Stream, remove_trend: bool = True,
           remove_mean: bool = True, filter_type: str = None,
           **kwargs) -> None:
    """
    Filter an obspy stream using frequent methods. Can remove the mean,
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


# remove response using inv or RESP file
def remove_response_inv(inv: Union[Inventory, str], st: Stream,
                        starttime: UTCDateTime = None,
                        endtime: UTCDateTime = None,
                        output: str = "DISP", **kwargs) -> None:
    """
    Remove the response from obspy stream object using an inventory object
    :param inv: Obspy Inventory object or path to a staXML
    :type inv: Inventory or str
    :param st: Obspy Stream object
    :type st: Stream
    :param starttime: Starttime of data. Used to ensure correct response
    :type starttime: UTCDateTime
    :param endtime: Endtime of data. Used to ensure correct response
    :type endtime: UTCDateTime
    :param output: Output Units (DISP (displacment [m]), VEL (velocity [m/s]),
                   ACC (acceleration [m/s**2]))
    :type output: str
    :param **kwargs: Keyword arguments passed to obspy Trace.remove_response
    :return: None
    """
    if isinstance(inv, str):
        inv = read_inventory(inv)

    if starttime and endtime:
        inv = inv.select(starttime=starttime, endtime=endtime)

    st.remove_response(inventory=inv, output=output, **kwargs)


def remove_response_resp(resp: str, st: Stream, output: str = 'DIS',
                         pre_filt: tuple = None, **kwargs) -> None:
    """
    Remove the response from an obspy stream using a RESP file
    :param resp: filename of response file
    :type resp: str
    :param st: Obspy stream
    :type st: Stream
    :param output: Output Units (DISP (displacment [m]), VEL (velocity [m/s]),
                   ACC (acceleration [m/s**2]))
    :type output: str
    :param pre_filt: Filter band to apply before deconvolution. See obspy
        simulate_seismometer. Example: (0.005, 0.006, 30.0, 35.0) Default: None
    :type prefilt: tuple
    :param kwargs: kwargs to be passed onto Obspy stream.simulate
    """
    seedresp = {'filename': resp,
                'units': output}

    st.simulate(paz_remove=None, pre_filt=pre_filt, seedresp=seedresp,
                **kwargs)
