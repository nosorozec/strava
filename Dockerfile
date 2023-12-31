FROM python:3

WORKDIR /usr/src/
RUN git clone https://github.com/nosorozec/strava.git

WORKDIR /usr/src/strava
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]