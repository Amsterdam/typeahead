Typeahead service 
==

Typeahead searches accross Datapunt APIs.

Run on your machine using:

```shell
$ pip install git+https://github.com/Amsterdam/typeahead
$ typeahead --config example.config.yml
``` 

Development / Local Testing
===

```shell
$ git clone git@github.com:Amsterdam/typeahead.git
$ cd typeahead

# create a virtualenv, then...

$ pip install -e .[dev,test]
$ typeahead --config example.config.yml
```

Design
===

Search endpoint
---

The root of the application, '/', is the search endpoint. It supports a `q` parameter only. Also see the info on our
OpenAPI spec below.

Note that the order of the results reflect the order of the endpoints in the configuration. The importance of the order
of the results is an artefact of a design mistake we have to live with for now.

Also note that the content type of the response bears slight resemblance to HAL JSON, but really isn't. This is again
due to 

Setuptools
---

Typeahead is an installable Python module. After installing (see example above), it provides the `typeahead` command,
which executes the `typeahead.main` module. See `setup.py` for all settings.

Async HTTP
---

Typeahead uses [asyncio](https://docs.python.org/3/library/asyncio.html) and runs [uvloop](https://github.com/MagicStack/uvloop)
as its eventloop. We use [aiohttp](https://aiohttp.readthedocs.io) as both http server, to serve requests on many
concurrent connections, and http client, to fetch search results from downstream endpoints in parallel.

In `typeahead.application` you can find our `aiohttp.web.Application`, including the routes. Note that we ship some
CORS-related code in `typeahead.application` that will hopefully soon be provided externally.

In `typeahead.handlers.*` you find the handlers for all endpoints.

Configuration
---

Configuration is provided through a configuration file in YAML format. The JSON schema is provided in
`typeahead.config_schema.yml`.

Module `typeahead.config` provides a `load(path)` mathod to load configuration. It will read the yaml, interpolate
placeholders with the environment, validate the schema and then return the loaded configuration. This greatly reduces
the need for validation of the provided configuration.

Docker, Jenkins, make
---

At Amsterdam, we run the code in a docker container. Our deployment pipeline is described in the provided `Jenkinsfile`.
Use the `Makefile` for repetitive tasks, such as cleaning up and running tests.

Metrics
---

Typeahead publishes [Prometheus](https://prometheus.io/) metrics on the `/metrics` endpoint. Metrics include:

| metric | type | labels |
| --- | --- | --- |
| request_processing_seconds | summary |  |
| search_exceptions_total | counter | endpoint, exc_type |
| search_responses_total | counter | endpoint, status |

Note that this endpoint will always run directly under the root, and will not keep the baseurl in mind. This allows us
to publish the metrics only internally.

OpenAPI
---

Typeahead publishes its own API on the `/openapi` endpoint.
