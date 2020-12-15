FROM amsterdam/python
    WORKDIR /root/app
    COPY . /root/app/
    RUN pip install .

COPY typeahead.yml /etc/typeahead.yml
