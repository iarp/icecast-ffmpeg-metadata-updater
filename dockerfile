FROM python:3.14-alpine

WORKDIR /usr/src/app

COPY helpers.py settings.py updater.py .

CMD ["python", "./updater.py"]
