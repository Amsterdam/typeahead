FROM amsterdam/docker_python:latest
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

ENV CONSUL_HOST=${CONSUL_HOST:-notset}
ENV CONSUL_PORT=${CONSUL_PORT:-8500}

WORKDIR /app
EXPOSE 8080

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt \
 && adduser --system typeahead \
 && addgroup --system typeahead

COPY . /app/
RUN chmod 755 /app/check_health.sh \
 && chmod 755 /app/ignite.sh

USER typeahead
CMD /app/ignite.sh
