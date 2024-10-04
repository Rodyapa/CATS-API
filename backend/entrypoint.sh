cd cats_api/
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py load_test_data_from_csv
python manage.py collectstatic --no-input
cp -r /app/cats_api/collected_static/. /backend_static/static/
gunicorn cats_api.wsgi:application --bind 0.0.0.0:8000