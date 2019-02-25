prometheus-build:
	docker build prometheus -t prometheus

store-build:
	docker build service -t store

build: store-build prometheus-build

run: build
	docker-compose up -d

stop:
	docker-compose stop

hello:
	curl localhost:8000/checkout | jq

metrics:
	curl http://localhost:9090/api/v1/query\?query\=payment_latency_seconds_total | jq

clean: stop
	docker-compose rm -f

test:
	python test.py

.PHONY: hello metrics