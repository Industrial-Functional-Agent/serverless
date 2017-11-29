export ZIP_FILE='JoongoToSlack.zip'
export PYTHON_VERSION='python3.6'
export VIRTUALENV='venv_lambda'
export PHANTOM='phantomjs-2.1.1-linux-x86_64'
export PHANTOM_ZIP='phantomjs-2.1.1-linux-x86_64.tar.bz2'

# Clean up
rm -rf $VIRTUALENV
rm $ZIP_FILE
rm -rf $PHANTOM

tar -xjvf $PHANTOM_ZIP

# Setup fresh virtualenv and install requirements
virtualenv --python=$PYTHON_VERSION --no-site-packages $VIRTUALENV
source $VIRTUALENV/bin/activate
pip install -r requirements-lambda.txt
deactivate

# Zip dependencies from virtualenv, and main.py
cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../
zip -g $ZIP_FILE main.py
zip -g $ZIP_FILE crawling.py
# zip -g $ZIP_FILE headless-chromium
# zip -g $ZIP_FILE chromedriver
zip -g -r9 $ZIP_FILE $PHANTOM
