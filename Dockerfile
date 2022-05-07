FROM python:3.10

WORKDIR /usr/src/app
COPY . .

# Install requirements
RUN pip install -r requirements.txt