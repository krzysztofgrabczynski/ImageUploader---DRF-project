FROM python:3.11

ENV DJANGO_SETTINGS_MODULE core.settings

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"] 