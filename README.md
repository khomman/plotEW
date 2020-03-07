# PlotEW

Convenience library and command line script for quickly retrieving and plotting data from an
earthworm wave server.  Built using Obspy and Click

## Installation

It is recommended to use a virtual environment. You can follow instructions for
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
or [venv](https://docs.python.org/3.6/library/venv.html#module-venv).

You can then clone from git:
```bash
git clone https://github.com/khomman/plotEW.git /path/to/plotEW
```

and install using pip or setup.py:
```bash
cd /path/to/plotEW
pip install .
```
or
```bash
cd /path/to/plotEW
python setup.py install
```

## Usage

PlotEW can be used to quickly investigate waveforms found in an earthworm
wave server.  You must provide the IP address and port number of the earthworm
wave server.  To do this you must provide the the --host and --port command
for every action.
```
bash
plotEW --host ew.server.ip --port 11111 plotEW_command
```

Alternatively, you can you can use the `config` command and plotEW will remember the host and port
values for the future.
```
bash
plotEW config
```

config will prompt you for the earthworm wave server ip and port then save the values in a config file
for future use.

The current plotEW commands are as follows:

**1:** plotEW config
        - Sets the earthworm wave server IP and port in the program for future
            use.

**2:** plotEW plot
        - Get data from an earthworm wave server and creates a simple waveform plot.

**3:** plotEW plot_helicorder
        - Get data from an earthworm wave server and creates a 24-hour helicorder style plot
          for the given time ranges.

**4:** plotEW save_waveforms
        - Get data from an earthworm wave server and save to disk as any obspy-supported format.


The `plot`, `plot_helicorder`, and `save_waveforms` commands also allow getting data from
[IRIS](https://www.iris.edu/hq/) using the --from_iris flag.


Please use the --help function for more information.
```
bash
plotEW --help
```

And for command-specific help
```
bash
plotEW plot --help
```


