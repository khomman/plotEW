import click

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
@click.option('-ts', '--starttime', required=True,
              help="Starttime for plotting")
@click.option('-tf', '--endtime', help="Endtime for plotting")
@click.option('-d', '--duration', type=int,
              help="Length of seismogram to (seconds)"
              "Overrides endtime flag")
@click.option('-s', '--station', required=True, help="SEED id for station")
@click.option('-bp', '--filter', nargs=2, type=float, help="Values for "
              "minimum and maximum frequency for bandpass filter")
@click.option('-f', '--filename', help="filename to save to")
@click.pass_context
def plot(ctx, starttime, endtime, duration, station, filter, filename):
    host = ctx.obj['host']
    port = ctx.obj['port']

    if not host or not port:
        raise RuntimeError("You must define the host and port to the "
                           "earthworm wave server. Type plotEW --help for "
                           "more information")

    if starttime and endtime:
        starttime = UTCDateTime(starttime)
        endtime = UTCDateTime(endtime)

    if starttime and duration:
        starttime = UTCDateTime(starttime)
        endtime = starttime + duration

    client = plotEW.init_client(host, int(port))
    st = plotEW.get_waveforms(client, station, starttime, endtime)

    if filter:
        plotEW.filter(st, filter_type='bandpass',
                      freqmin=filter[0],
                      freqmax=filter[1])
    plotEW.plot_stream(st, outfile=filename)


@main.command('plot_helicorder', help="Plot a helicorder style plot. "
              "Can provide a start and/or end time or specify the --last_day "
              "flag to plot the last 24 hours of data.  If starttime is "
              "specified but no end time then the endtime will be calculated "
              "to be 1 day after starttime. The behavior is similiar if "
              "endtime is provided but not starttime.")
@click.option('-s', '--station', required=True, help="SEED id for station")
@click.option('-ts', '--starttime', help="Starttime for plotting")
@click.option('-tf', '--endtime', help="Endtime for plotting")
@click.option('-bp', '--filter', nargs=2, type=float, help="Values for "
              "minimum and maximum frequency for bandpass filter")
@click.option('-f', '--filename', help="filename to save to")
@click.option('--last_day', is_flag=True, help="Plot the last 24 hours of "
                                               "data")
@click.pass_context
def plot_helicorder_recent(ctx, station, starttime, endtime, filter,
                           filename, last_day):
    host = ctx.obj['host']
    port = ctx.obj['port']

    if not host or not port:
        raise RuntimeError("You must define the host and port to the "
                           "earthworm wave server. Type plotEW --help for "
                           "more information")

    if not last_day and not starttime and not endtime:
        raise RuntimeError("You must provide either start and end times or "
                           "the --last_day flag")

    if last_day:
        cur_time = UTCDateTime.now()
        endtime = UTCDateTime(f"{cur_time.date}:{cur_time.hour}:00:00")
        starttime = endtime - 86400

    if starttime and not endtime:
        starttime = UTCDateTime(starttime)
        endtime = starttime + 86400

    if endtime and not starttime:
        endtime = UTCDateTime(endtime)
        starttime = endtime - 86400

    chan = station.split('.')[-1]
    if chan[0] != "L":
        print("High sample rate data may take a minute to gather...")
        print("Consider using lower sample rate data for faster plotting")

    client = plotEW.init_client(host, int(port))
    st = plotEW.get_waveforms(client, station, starttime, endtime)
    title = (f'{st[0].id}  {starttime.strftime("%Y-%m-%dT%H:%M:%S")} '
             f' - {endtime.strftime("%Y-%m-%dT%H:%M:%S")}')

    if filter:
        plotEW.filter(st, filter_type='bandpass', freqmin=filter[0],
                      freqmax=filter[1])

    plotEW.plot_helicorder(st, outfile=filename, title=title,
                           color=['k', 'r', 'g', 'b'], merge=True)


@main.command('save_waveforms', help="Download waveforms from an earthworm"
              "wave server")
@click.option('-s', '--station', required=True, help="Station to download")
@click.option('-ts', '--starttime', required=True,
              help="Starttime for plotting")
@click.option('-tf', '--endtime', help="Endtime for plotting")
@click.option('-d', '--duration', type=int,
              help="Length of seismogram to (seconds)"
              "Overrides endtime flag")
@click.option('-bp', '--filter', nargs=2, type=float, help="Values for "
              "minimum and maximum frequency for bandpass filter")
@click.option('-f', '--format', default='MSEED', help="Format of downloaded "
              "data.  See obspy Stream.write for more information")
@click.pass_context
def save_waveforms(ctx, station, starttime, endtime, duration, filter,
                   format):
    host = ctx.obj['host']
    port = ctx.obj['port']

    if not host or not port:
        raise RuntimeError("You must define the host and port to the "
                           "earthworm wave server. Type plotEW --help for "
                           "more information")

    if starttime and endtime:
        starttime = UTCDateTime(starttime)
        endtime = UTCDateTime(endtime)

    if starttime and duration:
        starttime = UTCDateTime(starttime)
        endtime = starttime + duration

    client = plotEW.init_client(host, int(port))
    st = plotEW.get_waveforms(client, station, starttime, endtime)

    if filter:
        plotEW.filter(st, filter_type="bandpass", freqmin=filter[0],
                      freqmax=filter[1])
    for tr in st:
        tr.write(f'{tr.id}.{format}', format=format)


def run():
    main(obj={})
