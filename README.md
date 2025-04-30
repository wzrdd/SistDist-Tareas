# Requisitos
- Docker

# Ejecución

Cada ejecución corre todo el sistema, basta con:
```bash
docker compose up
```

Para parametrizar, los contenedores de traffic_generator y Redis se manejan con variables de entorno en el docker-compose.yaml. Las opciones son DISTRIBUTION={poission, pareto} y EVICTION_POLICY={LRU, LFU}
