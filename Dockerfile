FROM python:3.10-bullseye AS build
RUN python -m venv /venv

RUN apt-get -qy update && apt-get -qy install git && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ADD requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt



FROM python:3.10-slim-bullseye

RUN addgroup --gid 1337 app && adduser --uid 1337 --gid 1337 --disabled-password --gecos "App User" app

COPY --from=build /venv /venv
COPY ./src /app

RUN chown app:app /app

USER 1337:1337

WORKDIR /app

# ENV PATH="/venv/bin:$PATH"

CMD ["/venv/bin/python3", "agent.py"]

# RUN addgroup --gid 1337 app && adduser --uid 1337 --gid 1337 --disabled-password --gecos "App User" app

# COPY ./src/ /app

# COPY ./requirements.txt /app

# RUN pip install -r /app/requirements.txt

# RUN chown app:app /app

# USER 1337:1337

# WORKDIR /app

# CMD ["python", "agent.py"]

# End of Dockerfile
