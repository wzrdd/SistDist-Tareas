start-scrapping:
	docker compose up -d mongo scraper

run-filtering:
	docker compose down
	docker compose up -d data_filtering

run-processing:
	rm -rf ./data/output/*
	docker compose down
	docker compose up -d data_processing

run-visualization:
	docker compose up -d elasticsearch kibana
	@echo "Esperando que Elasticsearch esté listo..."
	@until curl -s http://localhost:9200 | grep -q "cluster_name"; do \
		echo "Elasticsearch no está listo aún..."; \
		sleep 3; \
	done
	@echo "Elasticsearch listo. Ejecutando uploader..."
	docker compose up uploader

prepare-all:
	@echo "Iniciando el scrapping de datos..."
	docker compose up -d mongo scraper
	@echo "Esperando 60 segundos para que el scraper recoja datos..."
	sleep 60
	@echo "Deteniendo scrapping..."
	docker compose down
	@echo "Iniciando el filtrado de datos..."
	docker compose up -d data_filtering
	@echo "Deteniendo filtrado..."
	docker compose down
	@echo "Borrando archivos de salida anteriores y procesando datos..."
	rm -rf ./data/output/*
	docker compose up -d data_processing
	@echo "Done!!"
