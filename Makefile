install:
	bash install.sh

reinstall:
	bash reinstall.sh

run_debug:
	uvicorn src.server:app --host 0.0.0.0 --port 8080 --reload

run:
	gunicorn src.server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

compose_up:
	docker-compose up -d

compose_down:
	docker-compose down

start_redis:
	docker-compose up redis -d

stop_redis:
	docker-compose down redis

compose_prod_up:
	docker-compose -f docker-compose.prod.yml up -d

compose_prod_down:
	docker-compose -f docker-compose.prod.yml down