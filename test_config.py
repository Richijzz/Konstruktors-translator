import configparser
import os
from configparser import ConfigParser

print('-------------------Configuration test script------------------')
print('Checking if config file exists')
assert os.path.isfile('config.ini') == True
print('Test OK')
print('-----------------------------------------------------------------------------')

config = ConfigParser()
config.read('config.ini')

print('Checking if data exist in config file')
assert config.has_option('api', 'api_key') == True
assert config.has_option('database', 'database_location') == True
print('Test OK')
print('-----------------------------------------------------------------------------')

print('Checking if yaml files exist')
assert os.path.isfile('translator.yaml') == True
assert os.path.isfile('migration.yaml') == True
print('Test OK')
print('-----------------------------------------------------------------------------')

print('Checking if required directories exist')
assert os.path.isdir('log') == True
assert os.path.isdir('migrations') == True
print('Test OK')
print('-----------------------------------------------------------------------------')

print('SUCCESS')
print('All tests has been passed')