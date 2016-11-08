FROM build.datapunt.amsterdam.nl:5000/atlas/python:latest
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1

WORKDIR /app
EXPOSE 8080

COPY . /app/
COPY /consul/client.json /etc/consul.d/config.json
COPY /typeahead.sudo /etc/sudoers.d/typeahead

RUN chmod 755 /app/check_health.sh \
 && chmod 755 /app/ignite.sh \
 && pip install --upgrade pip \
 && pip install uwsgi \
 && pip install --no-cache-dir -r requirements.txt \
 && adduser --system typeahead \
 && addgroup --system typeahead


USER typeahead
CMD /app/ignite.sh