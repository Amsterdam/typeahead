FROM amsterdam/python:3.8-buster AS builder
MAINTAINER datapunt@amsterdam.nl
WORKDIR /root/app

# Install dependencies first (so layer is cached for fast rebuilds)
COPY setup.py ./
RUN mkdir /root/app/src \
 && pip wheel --no-cache-dir --wheel-dir=/wheelhouse/ . \
 && rm -vf /wheelhouse/datapunt_typeahead* \
 && pip install --no-cache-dir /wheelhouse/*

# Copy all files, install complete project.
COPY . /root/app/
RUN pip install --find-links=/wheelhouse/ .

# Start runtime image
FROM amsterdam/python:3.8-slim-buster

# Copy python build artifacts from builder image
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

EXPOSE 8080
USER datapunt

CMD ["typeahead", "--config", "/etc/typeahead.yml"]
