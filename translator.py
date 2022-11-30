import sqlite3
import logging.config
import yaml
import configparser
import requests
import json
import urllib.parse

from configparser import ConfigParser

with open('translator.yaml', 'r') as stream:
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
    api_key = config.get('api', 'api_key')

    db_host = config.get('database', 'database_location')
except:
    logger.error('Error while reading from config file')
    exit()

logger.info('Config file read successful')

logger.info('Connecting to databse')
conn = sqlite3.connect(db_host)
logger.info('Connected to database')

cursor = conn.cursor()

print('Welcome to translator app! What do you want to do?')
is_running = True

def translate_text(text):
    cursor.execute('''SELECT * FROM translations WHERE originaltext = ?''', (text,))
    dbresult = cursor.fetchall()

    if len(dbresult) > 0:
        print('Translation from', dbresult[0][2], ':' , dbresult[0][3])
        return 0
    else:
        url = 'https://api-free.deepl.com/v2/translate?auth_key='
        target_lang = 'LV'
        translation_text = urllib.parse.quote(text)
        request = url + api_key + '&text=' + translation_text + '&target_lang=' + target_lang
        data = requests.get(request).json()
        logger.info('Inserting data into database')
        cursor.execute('''INSERT INTO translations (originaltext, language, translatedtext) VALUES (?, ?, ?)''', (text, data['translations'][0]['detected_source_language'], data['translations'][0]['text'],))
        conn.commit()
        print('Translation from', data['translations'][0]['detected_source_language'], ':' , data['translations'][0]['text'])
        return 0


if __name__ == '__main__':
    while is_running:
        print('1 - Translate text')
        print('2 - Exit')
        try:
            user_choice = int(input('> '))
        except:
            print('Please enter a number!')
            continue
        if user_choice == 1:
            text = input('Please enter your text to translate: ')
            translate_text(text)
        elif user_choice == 2:
            is_running = False
            print('See you soon!')
            exit()
        else:
            print('Wdym?')
