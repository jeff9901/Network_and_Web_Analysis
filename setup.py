from setuptools import setup, find_packages

setup(
    name = 'Status_monitor',
    version='0.1',
    install_requires=['Click',],
    py_modules=['Status_monitor'],
    entry_points='''
    [console_scripts]
    run=Status_monitor:cli
    '''
)
