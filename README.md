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
wave server.  To do this you can issue the command:
```
bash
plotEW config
```

config will prompt you for the information and save the values in a config file
for future use.

There are currently only three plotEW commands:

**1** plotEW config

**2** plotEW plot

**3** plotEW plot_helicorder


Please use the --help function for more information.
```
bash
plotEW --help
```


