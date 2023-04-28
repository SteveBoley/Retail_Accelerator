FROM python:3.7.3 as builder
WORKDIR /django_ecommerce_app
COPY requirements.txt /django_ecommerce_app

RUN pip install -r requirements.txt --no-cache-dir
COPY . /django_ecommerce_app/
# COPY static_in_env /django_ecommerce_app/static_in_env
EXPOSE 8000
# CMD ["python", "manage.py", "-y", "collectstatic"]
CMD ["python","manage.py", "runserver","0.0.0.0:8000"]
