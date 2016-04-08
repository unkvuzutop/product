
INIT (project have fixture with initial data and default user):

python manage.py syncdb --noinput; 
python manage.py migrate --noinput; 
python manage.py loaddata product/fixtures/users.json; 
python manage.py loaddata product/fixtures/product.json


default user:
username:  admin
password:  admin
