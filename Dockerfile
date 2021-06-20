FROM python:3.8.9

COPY . /

RUN apt-get update
RUN apt-get -y upgrade
RUN pip install -U -r /requirements.txt

ENTRYPOINT ["python3", "manage.py","runserver","0.0.0.0:8000"]
