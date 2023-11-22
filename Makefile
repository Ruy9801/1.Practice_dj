run:
	./manage.py runserver 

migrate:
	./manage.py makemigrations
	./manage.py migrate 

superuser:
	./manage.py createsuperuser 

celery:
	python -m celery -A config worker -l info