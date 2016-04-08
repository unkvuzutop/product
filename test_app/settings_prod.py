ALLOWED_HOSTS = ['unkvuzutop.webfactional.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_app',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '/path/to/project/test_app/product/static/',
)

STATIC_ROOT = '/path/to/static/root/'
