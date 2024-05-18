server.docker.build:
	docker-compose up -d --build --remove-orphans

server.docker.up:
	docker-compose up -d

server.docker.down:
	docker-compose down

server.docker.reup: server.docker.down server.docker.up

server.docker.rebuild: server.docker.down server.docker.build
