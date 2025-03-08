build:
	docker compose up --build

down:
	docker compose down

up:
	@docker compose down
	@docker compose up --build

run_scraper:
	docker compose exec scraper python -m scraper --max-scans 240 --only-type article
