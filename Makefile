start:
	docker-compose up

build:
	docker-compose up --build

rebuild:
	docker-compose up --build --no-cache

down:
	docker-compose down --rmi all --volumes