ARG dockerImage
FROM ${dockerImage} AS base

ARG projectHomeDirpath
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
WORKDIR /home
ENV PYTHONPATH=/home

# add custemization
FROM base AS layer1
RUN apt-get update -y &&\
    apt-get install libpq-dev python-dev gcc -y

COPY requirements*.txt /
RUN pip install --no-cache-dir -r /requirements-prd.txt

COPY ./app ${HOME}

COPY ./bin/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh"]
CMD [ "tail", "-f", "/dev/null"]
