ARG PYTHON_VERSION=3.11.1-alpine3.16
FROM python:$PYTHON_VERSION as builder
WORKDIR /

RUN apk add --no-cache g++ curl
RUN mkdir -p /root/.ssh
RUN python -m venv .venv \
	&& .venv/bin/pip install --no-cache-dir -U pip==22.3.1

ADD requirements.txt .
RUN .venv/bin/pip install --no-cache-dir -r ./requirements.txt
COPY . /user_authenticator

FROM python:$PYTHON_VERSION
WORKDIR /user_authenticator

RUN apk add curl
COPY --from=builder /user_authenticator /user_authenticator
COPY --from=builder /.venv /.venv
EXPOSE 8000


ENV PATH="/.venv/bin:$PATH"
ENV PYTHONPATH /srv/avis/

ENTRYPOINT ["python3", "entrypoint.py"]
