import os

from obspy import read, read_inventory
from obspy.clients.earthworm import Client

import pytest

import plotEW as pew


@pytest.fixture()
def stream():
    st = read('data/PE.PAKC..HHZ.MSEED')
    return st


@pytest.fixture()
def tmp_dir(tmpdir):
    p = tmpdir.mkdir('tstFig')
    return p


def test_init_client():
    client = pew.init_client('127.0.0.1', 16030)
    assert isinstance(client, Client)


def test_read_station_file():
    stas = pew.read_station_file('data/teststafile.txt')
    assert len(stas) == 3
    assert stas[0] == 'PE.PAKC..HHZ'
    assert stas[1] == 'IU.SSPA.10.HHN'
    assert stas[2] == 'LD.ALLY..HHZ'


def test_plot_helicorder(stream, tmp_dir):
    pew.plot_helicorder(stream[0], outfile=f'{tmp_dir}/PAKC_Heli.pdf')
    assert os.path.exists(f'{tmp_dir}/PAKC_Heli.pdf')


def test_plot_stream(stream, tmp_dir):
    pew.plot_stream(stream, outfile=f'{tmp_dir}/PAKC_Stream_Plot.pdf')
    assert os.path.exists(f'{tmp_dir}/PAKC_Stream_Plot.pdf')


def test_filter(stream):
    pew.filter(stream, filter_type="bandpass", freqmin=1, freqmax=10)
    assert len(stream) == 1
    assert len(stream[0].stats.processing) == 3
    assert 'demean' in stream[0].stats.processing[0]
    assert 'linear' in stream[0].stats.processing[1]
    assert 'filter' in stream[0].stats.processing[2]


def test_remove_response_inv(stream):
    # Test inventory as string
    pew.remove_response_inv('data/PAKC_test.xml', stream)
    assert len(stream[0].stats.processing) == 1
    assert 'remove_response' in stream[0].stats.processing[0]


def test_remove_response_inv_as_object(stream):
    inv = read_inventory('data/PAKC_test.xml')
    pew.remove_response_inv(inv, stream)
    assert len(stream[0].stats.processing) == 1
    assert 'remove_response' in stream[0].stats.processing[0]


def test_remove_response_inv_start_end_time(stream):
    pew.remove_response_inv('data/PAKC_test.xml', stream,
                            starttime=stream[0].stats.starttime,
                            endtime=stream[0].stats.endtime)
    assert len(stream[0].stats.processing) == 1
    assert 'remove_response' in stream[0].stats.processing[0]


def test_remove_response_resp(stream):
    pew.remove_response_resp('data/RESP.PE.PAKC.--.HHZ', stream)
    assert len(stream[0].stats.processing) == 1
    assert 'simulate' in stream[0].stats.processing[0]
