FROM alpine:3.7

MAINTAINER Security Team <securityteam@iriusrisk.com>

ADD . /threat

RUN apk add python3 git py3-pip nano \
&& git clone https://github.com/iriusrisk/iriusrisk-python-client-lib.git \
&& pip3 install iriusrisk-python-client-lib/iriusrisk-python-client-lib \
&& mkdir /volume \
&& cd threat \
&& pip3 install -r requirements.txt

WORKDIR threat
CMD find /volume/. -name \*.py -exec cp {} ./tests \; \
&& find /volume/. -name \*.yaml -exec cp {} . \; \
&& pytest --junitxml=/volume/result.xml --tb=line




