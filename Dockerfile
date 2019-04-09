FROM python:3.7.3-slim

WORKDIR /usr/src/mitmi

RUN pip3 install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . .

EXPOSE 5000

ENTRYPOINT [ "flask" ]

CMD ["run", "--host=0.0.0.0"]