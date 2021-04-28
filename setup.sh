# if pip doesn't work use pip3
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
touch store.db