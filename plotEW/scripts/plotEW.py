import click

import matplotlib.pyplot as plt
from obspy import UTCDateTime

import plotEW as pew


@click.group()
def cli():
    pass


@cli.command('plot')
@click.option('-h', '--host', required=True)
@click.option('-p', '--port', required=True)
@click.option('-ts', '--starttime')
@click.option('-tf', '--endtime')
@click.option('-s', '--station')
@click.option('-f', '--filename')
def plot(host, port, starttime, endtime, station, filename):
    client = pew.init_client(host, int(port))
    st = pew.get_waveforms(client, station, UTCDateTime(starttime),
                           UTCDateTime(endtime))
    ax = pew.plot_stream(st)
    plt.show()


def run():
    cli(obj={})
