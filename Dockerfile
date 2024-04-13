FROM python:3.12.2

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install poetry

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]