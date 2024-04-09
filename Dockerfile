FROM python:3.11-slim

ENV APP_HOME /hw6

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "main.py"]