FROM amsterdam/python:3.7-buster
    WORKDIR /root/app
    COPY . /root/app/
    RUN pip install .

COPY typeahead.yml /etc/typeahead.yml
