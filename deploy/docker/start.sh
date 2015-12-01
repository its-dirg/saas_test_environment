#!/bin/sh

# copy all config from mounted volume
cp -r /mnt/config/. /tmp/src/saas/example/

# generate metadata for front- (IdP) and back-end (SP) and write it to mounted volume
make_saml_metadata.py -o /mnt/config proxy_conf.yaml

# start the proxy
exec gunicorn -b0.0.0.0:${PROXY_PORT} --keyfile https.key --certfile https.crt saas.proxy_server:app