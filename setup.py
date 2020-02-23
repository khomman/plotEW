from setuptools import find_packages, setup

setup(
    name='plotEW',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'obspy',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'plotEW=plotEW.scripts.plotEW:run'
        ]
    }
)