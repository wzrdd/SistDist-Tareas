# Requisitos
- Docker
- Make

# Ejecución
El pipeline lo dividí en dos pasos: 1) prepare-all que scrappea, almacena y procesa con PIG, 2) run-visualization que levanta ES + Kibana y corre un contenedor que toma la salida del procesamiento con PIG y lo sube a ES. El servicio de Kibana queda disponible en http://localhost:5601/ por defecto en el docker-compose (hardcodeado).

```bash
make prepare-all
make run-visualization
```
