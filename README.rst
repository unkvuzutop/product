
INIT (project have fixture with initial data and default user):
====

+ python manage.py syncdb --noinput; 
+ python manage.py migrate --noinput; 
+ python manage.py loaddata product/fixtures/* 

or you can use make file:

+ make syncdb

+ make test

+ make run


default user:
====
+ username:  admin
+ password:  admin
