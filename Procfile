release: cd compass_oauth_proxy && python manage.py migrate
web: cf compass_oauth_proxy && gunicorn compass_oauth_proxy.wsgi
