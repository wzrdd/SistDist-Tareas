start-scrapping:
	docker compose up -d mongo scraper

run-filtering:
	docker compose down
	docker compose up -d data_filtering

run-processing:
	rm -rf ./data/output/*
	docker compose down
	docker compose up -d data_processing
