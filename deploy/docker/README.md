# Setting up SAAS (Software as a Service) proxy from Docker container

The [SATOSA proxy](https://github.com/its-dirg/SATOSA) can be used to "hide" many underlying Identity
Providers (IdPs) from a Service Provider (SP) which only supports interacting with a single IdP. 
To the service provider the proxy acts as a single IdP while it forwards any authentication
requests to an actual IdP, selected by the user through a discovery service:

    [Service Provider] <-> [IdP|Proxy|SP] <-> [IdPs]

## Configuration
Examples of all files necessary for configuring the proxy can be found in `deploy/docker/env`.

### Volume binding
All configuration is managed by mounting a host directory as a volume under `/mnt/config` in the
Docker container.
The directory should have the following structure:

    <host dir>/
    ├── backend.crt
    ├── backend.key
    ├── frontend.crt
    ├── frontend.key
    ├── https.crt
    ├── https.key
    ├── plugins
    │   ├── saml2_backend.py
    │   └── saml2_frontend.py
    ├── proxy_conf.yaml
    └── sp.xml

where

* `{backend, frontend}.{crt, key}` is the cert+key for the SAML SP and IdP of the proxy
* `{https}.{crt, key}` is the cert+key for HTTPS
* `plugins/saml2_{backend, frontend}.py` is the configuration of the SAML SP and IdP of the proxy
* `proxy_conf.yaml` is the configuration of the proxy
* `sp.xml` is the Service Providers SAML metadata


### Proxy configuration: `proxy_conf.yaml`

The following parameters *MUST* be configured:

* `BASE`: publicly reachable URL of the running Docker container, *must* be HTTPS.
* `USER_ID_HASH_SALT`: random string to be used internally by the proxy when hashing user identifiers
 
The proxy uses a "secure cookie" (which is only sent over HTTPS) to preserve state, which is why
the proxy must use HTTPS. The Docker container uses [gunicorn](http://gunicorn.org/), which supports
HTTPS, to run the proxy's WSGI application. `gunicorn` is started with the certificate
in `https.crt` and the associated private key in `https.key`. 
    

### Backend configuration: `plugins/saml2_backend.py`

The following parameters *MUST* be configured:

* `sp_config["disco_srv"]`: url of discovery service to let the user choose the IdP
* `sp_config["metadata"]`: url or path to metadata for backing IdPs, see [pysaml2 metadata configuration](https://github.com/rohe/pysaml2/blob/master/doc/howto/config.rst#metadata).

## SAML metadata

The Docker container will create SAML metadata at startup and write it to the mounted host directory.

* Service Provider and proxy frontend: the Service Provider needs the metadata of the proxy frontend,
  written to `<host dir>/Saml2IDP_frontend_metadata.xml`, and the proxy frontend needs the Service Providers metadata in `sp.xml` mounted in the container.
* Proxy backend and backing IdPs: the backing IdPs need the metadata of the proxy backend (which
  acts as a SAML SP), written to `<host dir>/Saml2_backend_metadata.xml`, and the proxy backend needs the metadata of all backing IdPs (see [above section](#saml-metadata)). 

## Docker

Building an image from the Dockerfile:
    
    docker build -t <image name> deploy/docker

Starting a container from the image:

     docker run [-d] -p <port on host>:<proxy_port> -v <host directory>:/mnt/config -e PROXY_PORT=<proxy_port> <image name>

    