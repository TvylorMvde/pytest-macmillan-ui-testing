FROM python:3.9.2-slim

RUN apt-get -y update

RUN apt-get -y install -yqq unzip

RUN apt-get -y install wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN apt-get -y update

RUN wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip

RUN unzip chromedriver.zip

RUN chmod +rwx chromedriver

ENV DISPLAY=:99

# chromedriver -d .
# ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

# COPY chromedriver .
COPY test_module.py .

CMD ["pytest", "test_module.py"]




 







