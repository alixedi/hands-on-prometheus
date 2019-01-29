FROM python:3.7-alpine

COPY Pipfile* /

RUN pip install -U pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ADD hello /hello
CMD ["gunicorn", "hello", "-b 0.0.0.0:8000"]
