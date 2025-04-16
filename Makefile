start:
	docker compose up --build -d
stop:
	docker compose down
get-token:
	docker logs spark-jupyter