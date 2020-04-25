FROM python:3.8.2-alpine3.10

WORKDIR /app

RUN python3 -m pip install \
        requests

COPY ./main.py ./main.py

ENTRYPOINT [ "/app/main.py" ]
