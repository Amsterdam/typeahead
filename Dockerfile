FROM amsterdam/python
    WORKDIR /root/app
    COPY . /root/app/
    RUN pip install .