release: sh -c 'cd mysite && python manage.py makemigrations pagos && python manage.py migrate'
web: sh -c 'cd mysite && gunicorn mysite.wsgi --log-file -'