################################################################################
FROM python:3.6.8-alpine3.9 AS base

################################################################################
FROM base AS build

RUN apk add build-base zeromq-dev

RUN python -m venv /venv

RUN python -m pip install --upgrade pip

ADD requirements.txt .

#Passing secret into a stage that is not the last stage in a multi-stage pipeline is safe
ARG PACKAGE_REPO

RUN /venv/bin/pip install --extra-index-url="${PACKAGE_REPO}" -r requirements.txt

################################################################################
FROM base AS runtime

RUN apk --no-cache add zeromq

COPY --from=build /venv /venv

ADD data_generator/locustfile.py /app/

################################################################################
FROM runtime AS test

RUN /venv/bin/pip install pytest pytest-cov

ADD tests /app/tests

RUN cd /app && /venv/bin/python -m pytest --doctest-modules --junitxml=./tests/junit/test-results.xml --cov=./data_generator ./tests/ --cov-report=xml:./tests/junit/coverage.xml --cov-report=html:./tests/junit/cov_html

################################################################################
FROM runtime AS production

EXPOSE 8089 5557 5558

WORKDIR /app
ENTRYPOINT ["/venv/bin/locust"]
