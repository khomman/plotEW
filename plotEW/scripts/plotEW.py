import click

import matplotlib.pyplot as plt
from obspy import UTCDateTime

import os
import plotEW


@click.group()
@click.option('-h', '--host', help="IP address to earthworm wave server")
@click.option('-p', '--port', help="Port of earthworm wave server")
@click.option('-c', '--config_file', default="~/.plotEW.cfg")
@click.pass_context
def main(ctx, host, port, config_file):
    """
    Small convenience command line too for plotting data from an
    earthworm wave server.
    You must supply an IP and port number for the earthworm wave server
    """
    filename = os.path.expanduser(config_file)

    if not host and os.path.exists(filename):
        with open(filename) as f:
            host, port = f.read().split('\n')

    ctx.obj = {
        'host': host,
        'port': port,
        'config_file': filename
    }


@main.command(help="Prompts for an earthworm wave server IP and port number."
              "Saves the values to a config file in your home directory")
@click.pass_context
def config(ctx):
    config_file = ctx.obj['config_file']

    host = click.prompt("Please enter the IP address for the earthworm "
                        "wave server", default=ctx.obj.get('host', ''))

    port = click.prompt("Please enter the port number for the earthworm "
                        "wave server", default=ctx.obj.get('port', ''))

    with open(config_file, 'w') as f:
        f.write(f"{host}\n{port}")


@main.command('plot')
@click.option('-ts', '--starttime', help="Starttime for plotting")
@click.option('-tf', '--endtime', help="Endtime for plotting")
@click.option('-s', '--station', help="SEED id for station")
@click.option('-p', '--process_data', nargs=2, type=float, help="Values for "
              "minimum and maximum frequency for bandpass filter")
@click.option('-f', '--filename', help="filename to save to")
@click.pass_context
def plot(ctx, starttime, endtime, station, process_data, filename):
    host = ctx.obj['host']
    port = ctx.obj['port']

    if not host or not port:
        raise RuntimeError("You must define the host and port to the "
                           "earthworm wave server. Type plotEW --help for "
                           "more information")

    client = plotEW.init_client(host, int(port))
    st = plotEW.get_waveforms(client, station, UTCDateTime(starttime),
                              UTCDateTime(endtime))

    if process_data:
        plotEW.basic_processing(st, filter_type='bandpass',
                                freqmin=process_data[0],
                                freqmax=process_data[1])
    plotEW.plot_stream(st, outfile=filename)


def run():
    main(obj={})
