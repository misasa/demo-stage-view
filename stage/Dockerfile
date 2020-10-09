FROM python:3
RUN apt-get update \
&& apt-get -y install mosquitto-clients \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "/usr/src/app/demo.py" ]