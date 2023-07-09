FROM python

COPY ./api/src/requirements.txt /tmp

RUN apt-get update
RUN apt install -y pulseaudio alsa-utils portaudio19-dev
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /api
CMD ["python", "app.py"]