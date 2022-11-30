import sqlite3
import logging.config
import yaml
import configparser
from sqlite3 import Error
import os

from configparser import ConfigParser

with open('migration.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

logging.config.dictConfig(config)

#Creating logger file
logger = logging.getLogger('root')
logger.info('Translator started')

try:
    #Reading config file
    logger.info('Start reading from config file')
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_host = config.get('database', 'database_location')
except:
    logger.error('Error while reading from config file')
    exit()

logger.info('Config file read successful')

logger.info('Connecting to databse')
conn = sqlite3.connect(db_host)

if conn:
    logger.info('Connected to database')
else:
    logger.error('Connection failed')

cursor = conn.cursor()

# Check if table exists
def mysql_check_if_table_exists(table_name):
    records = []
    try:
        result  = cursor.execute('''
            SELECT 
                name
            FROM 
                sqlite_schema
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%'
        ''')
        conn.commit()
    except Error as e :
        logger.error("query: " + "SHOW TABLES LIKE '" + str(table_name) + "'")
        logger.error('Problem checking if table exists: ' + str(e))
        pass

    if str(table_name) in records:
        return True
    else:
        return False

migrations_list = []
# Reading all migration file names into an array
cur_dir = os.getcwd()
migrations_files_list = os.listdir(cur_dir + "/migrations/")
for f_name in migrations_files_list:
	if f_name.endswith('.sql'):
		migrations_list.append(f_name)

# Sorting list to be processed in the correct order
migrations_list.sort(reverse=False)

counter = 0

for migration in migrations_list:
    with open(cur_dir + "/migrations/" + migration,'r') as file:
        migration_sql = file.read()
        logger.debug(migration_sql)
        logger.info("Executing: " + str(migration))
        try:
            cursor.execute(migration_sql)
            conn.commit()
            logger.info('Migrated ' + str(migration))
        except Error as e:
            logger.error('Migration failed ' + str(e))