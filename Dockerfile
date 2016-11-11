FROM build.datapunt.amsterdam.nl:5000/atlas/python:latest
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1

WORKDIR /app
EXPOSE 8080

COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install uwsgi \
 && pip install --no-cache-dir -r requirements.txt \
 && adduser --system typeahead \
 && addgroup --system typeahead

COPY ./consul/ /etc/consul.d/
COPY /typeahead.sudo /etc/sudoers.d/typeahead

COPY . /app/
RUN chmod 755 /app/check_health.sh \
 && chmod 755 /app/ignite.sh

USER typeahead
CMD /app/ignite.sh