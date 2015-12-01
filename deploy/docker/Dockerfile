FROM ubuntu:14.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-dev \
    build-essential \
    python3-pip \
    libffi-dev \
    libssl-dev \
    xmlsec1 \
    libyaml-dev

RUN pip3 install --src /tmp/src -e git+https://github.com/its-dirg/saas_test_environment@6214995#egg=saas && \
    pip3 install -r /tmp/src/saas/requirements.txt

COPY start.sh /tmp/
WORKDIR /tmp/src/saas/example/
ENTRYPOINT ["/tmp/start.sh"]
