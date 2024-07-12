ARG dockerImage
FROM --platform=linux/amd64  ${dockerImage}

ARG projectHomeDirpath
ENV PYTHONUNBUFFERED 1
ENV HOME=/app
WORKDIR ${HOME}
ENV PYTHONPATH=${HOME}

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./app /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "tail", "-f", "/dev/null" ]
