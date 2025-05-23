# Kafka

## Setup Python

### install pyenv

```bash
curl -fsSL https://pyenv.run | bash
```

zsh:

```
alias brew='env PATH="${PATH//$(pyenv root)\/shims:/}" brew'
```

### install python

```
export LDFLAGS="-L/opt/local/lib"
export CPPFLAGS="-I/opt/local/include"
sudo pyenv install 3.11.4
```

### Create pyenv

```bash
pyenv virtualenv 3.11.4 sample_kafka_consumer
pyenv local sample_kafka_consumer
```

```bash
pip install -r requirements.txt
```

## Run

```bash
make run
```

```bash
make runtls
```

## Send Message

http://localhost:9090/sendmessage

## Doc

https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html

# Get SSL Certs

# kubectl -n strimzi get secret my-cluster-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt


```bash
kubectl -n strimzi get secret test -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
kubectl -n strimzi get secret test -o jsonpath='{.data.user\.key}' | base64 -d > user.key
kubectl -n strimzi get secret test -o jsonpath='{.data.user\.crt}' | base64 -d > user.crt
```
