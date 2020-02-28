import os

from obspy import read
from obspy.clients.earthworm import Client


import plotEW as pew


def test_init_client():
    client = pew.init_client('127.0.0.1', 16030)
    assert isinstance(client, Client)


def test_read_station_file():
    stas = pew.read_station_file('data/teststafile.txt')
    assert len(stas) == 3
    assert stas[0] == 'PE.PAKC..HHZ'
    assert stas[1] == 'IU.SSPA.10.HHN'
    assert stas[2] == 'LD.ALLY..HHZ'


def test_plot_helicorder():
    st = read('data/PE_PAKC_Z.MSEED')
    pew.plot_helicorder(st[0], outfile="data/PAKC_Heli.pdf")
    assert os.path.exists('data/PAKC_Heli.pdf')


def test_plot_stream():
    st = read('data/PE_PAKC_Z.MSEED')
    pew.plot_stream(st, outfile='data/PAKC_Stream_Plot.pdf')
    assert os.path.exists('data/PAKC_Stream_Plot.pdf')


def test_filter():
    st = read('data/PE_PAKC_Z.MSEED')
    pew.filter(st, filter_type="bandpass", freqmin=1, freqmax=10)
    assert len(st) == 1
    assert len(st[0].stats.processing) == 3
    assert 'demean' in st[0].stats.processing[0]
    assert 'linear' in st[0].stats.processing[1]
    assert 'filter' in st[0].stats.processing[2]


def test_remove_response_inv():
    pass


def test_remove_response_resp():
    pass


def teardown():
    print('teardown')


if __name__ == "__main__":
    pass
