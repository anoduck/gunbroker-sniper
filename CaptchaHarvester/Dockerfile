# For CaptchaHarvester

From alpine:edge

EXPOSE 5000

WORKDIR /srv/harvester

RUN apk update && apk add python3 \
	py3-pip

RUN pip install captcha-harvester

ENTRYPOINT harvester -H 0.0.0.0 -p 5000 -d gunbroker.com -k 6LeyID0aAAAAAOVFOxIySt6jjDofMGAM08yesbBn -v recaptcha-v2