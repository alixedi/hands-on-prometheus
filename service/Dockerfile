FROM python:3.7-alpine

COPY Pipfile* /

RUN pip install -U pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ADD store /store
ENV FLASK_APP store
CMD ["flask", "run", "-h 0.0.0.0", "-p 8000"]
