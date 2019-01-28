prometheus-build:
	docker build prometheus -t prometheus

hello-build:
	docker build hello -t hello

build: hello-build prometheus-build

run: build
	docker-compose up -d

stop:
	docker-compose stop

hello:
	curl localhost:8000/${NAME} | jq

metrics:
	curl http://localhost:9090/api/v1/query\?query\=hello_count_total | jq

clean: stop
	docker-compose rm -f

test:
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py & \
	python test_hello.py

.PHONY: hello metrics