export ZIP_FILE='JoongoToSlack.zip'
export PYTHON_VERSION='python3.6'
export VIRTUALENV='venv_lambda'
export PHANTOM='phantomjs/phantomjs-2.1.1-linux-x86_64'
export PHANTOM_ZIP='phantomjs/phantomjs-2.1.1-linux-x86_64.tar.bz2'

rm -rf $VIRTUALENV
rm $ZIP_FILE

rm -rf $PHANTOM
tar -xjvf $PHANTOM_ZIP --directory phantomjs

virtualenv --python=$PYTHON_VERSION --no-site-packages $VIRTUALENV
source $VIRTUALENV/bin/activate
pip install -r requirements-lambda.txt
deactivate

cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../
zip -g $ZIP_FILE *.py

zip -g -r9 $ZIP_FILE $PHANTOM