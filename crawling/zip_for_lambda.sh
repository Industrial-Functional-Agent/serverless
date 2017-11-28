export ZIP_FILE='JoongoToSlack.zip'
export PYTHON_VERSION='python3.6'
export VIRTUALENV='venv_lambda'

# Clean up
rm -rf $VIRTUALENV
rm $ZIP_FILE

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
