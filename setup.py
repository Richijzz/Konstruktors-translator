import pip
import importlib

print('------------------Translator app setup------------------')

print('Checking and installing required packeages.')
#Installing required packages
def install_package(package):
    try:
        importlib.import_module(package)
        print('Package already installed', package)
    except:
        print(package, 'Package not found. Installing...')
        pip.main(['install', package])
        print('Package installed.')

install_package('configparser')
install_package('logger')
install_package('yaml')

import configparser
from configparser import ConfigParser

#User input for configuration info

print('Now we need details about your app')
key = input('Enter DEEPL API key: ')
location = input('Please enterthe location of four database, for example /database/translator.db: ')
#Config creation
config = configparser.ConfigParser()

config['api'] = {'api_key': key}

config['database'] = {'database_location': location}
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print('-----------------------------------------------')
print('Config file created')
print('Setup cpmplete!')
print('-----------------------------------------------')