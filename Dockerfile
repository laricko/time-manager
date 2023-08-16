FROM python:3.11.4-slim

WORKDIR /app

COPY Pipfile* .
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --system --ignore-pipfile

COPY src .

CMD [ "flask", "run", "--debug", "--host=0.0.0.0", "--port=8000" ]

