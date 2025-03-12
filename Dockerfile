FROM python:3.11-slim

RUN set -x \
	&& DEBIAN_FRONTEND=noninteractive apt-get update --quiet \
	&& DEBIAN_FRONTEND=noninteractive apt-get upgrade --quiet --yes \
	&& DEBIAN_FRONTEND=noninteractive apt-get install --quiet --yes --no-install-recommends \
	apt-transport-https \
	bash \
	ca-certificates \
	curl \
	git \
	build-essential \
	software-properties-common \
	git \
	&& DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes \
	&& DEBIAN_FRONTEND=noninteractive apt-get clean

WORKDIR /app
COPY requirements.txt main.py ./
COPY pkg ./pkg/
RUN pip install -r requirements.txt

EXPOSE 9090
CMD ["python3","main.py"]
