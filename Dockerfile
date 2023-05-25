# Container image that runs your code
FROM alpine:3.14

# Install python & pip (3.14 repos use python 3.9)
RUN apk add --update --no-cache python3 py3-pip
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY ./processor.py /processor.py
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN chmod +x /processor.py

# install additional modules
COPY ./requirements.txt /requirements.txt
RUN pip3 install --ignore-installed -r /requirements.txt

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]