FROM python:3.11-slim

# WORKDIR /usr/src/strava/
# RUN git clone https://github.com/nosorozec/strava.git

# WORKDIR /usr/src/strava
ADD main.py strava.py finance.py requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD [ "python", "./main.py" ]