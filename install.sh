#!/bin/bash

echo "Python Translator app install script"
echo "-------------------------------------"

echo "Checking if required files exist"
if test -f "translator.yaml.dev"; then echo "File exists"; else echo "translator.yaml.dev not found"; exit 1; fi
if test -f "migration.yaml.dev"; then echo "File exists"; else echo "migration.yaml.dev not found"; exit 1; fi
if test -f "config.ini.template"; then echo "File exists"; else echo "config.ini.template not found"; exit 1; fi

echo "--------------------------------------"

echo "Renaming Files..."
mv translator.yaml.dev translator.yaml
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem copying translator.yaml.dev file"; exit 1; fi
mv migration.yaml.dev migration.yaml
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem copying migration.yaml.dev file"; exit 1; fi
mv config.ini.template config.ini
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem copying config.ini.template file"; exit 1; fi

echo "Running setup.py"
python3 setup.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Problems with setup.py"; exit 1; fi
python3 test_config.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Problems with test_config.py"; exit 1; fi
python3 test.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Problems with test.py"; exit 1; fi

echo "Running Database migrations"
python3 migration.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Problems with migration.py"; exit 1; fi

echo "------------------------------------------------------------------------"

echo "Setup successfull"
echo "To use translator app run: python3 translator.py"
