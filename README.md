# Kafka Consumer

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







## Start Kafka

```
docker exec -it kafka kafka-console-producer --topic test-topic --bootstrap-server localhost:9092
```

## Doc

https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
