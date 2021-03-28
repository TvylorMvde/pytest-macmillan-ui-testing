FROM python:3.9.2-slim

RUN apt-get -y update && \
    apt-get -y install -yqq unzip && \
    apt-get -y install wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get -y install ./google-chrome-stable_current_amd64.deb && \
    apt-get -y update && \
    wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip && \
    unzip chromedriver.zip && \
    chmod +rwx chromedriver

ENV DISPLAY=:99

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY test_module.py .

CMD ["pytest", "test_module.py"]




 







