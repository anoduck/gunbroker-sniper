# For CaptchaHarvester

FROM alpine:edge

ARG SITEKEY
ARG DOMAIN

EXPOSE 5000

WORKDIR /srv/harvester

RUN apk update && apk add python3 \
	py3-pip

RUN pip install captcha-harvester

ENTRYPOINT harvester -H 0.0.0.0 -p 5000 -d $DOMAIN -k $SITEKEY -v recaptcha-v2