FROM python:3.6.8-alpine3.9 AS build

ARG IMAGE_SERVER

RUN apk add build-base

RUN apk add zeromq-dev

RUN python -m venv /venv

ADD requirements.txt .

RUN PIP_EXTRA_INDEX_URL=${IMAGE_SERVER} /venv/bin/pip install -r requirements.txt

FROM python:3.6.8-alpine3.9 AS production

RUN apk add zeromq

COPY --from=build /venv /venv

ADD locustfile.py /

EXPOSE 8089 5557 5558

ENTRYPOINT ["/venv/bin/locust"]
