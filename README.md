# Requisitos
- Docker
- Make

# Ejecución

La ejecución se divide en 3 pasos discretos: 1) Scrapping, 2) Filtering y 3) Processing. Para esto se creó un makefile con estos 3 comandos en el siguiente orden:
```bash
make start-scrapping
make run-filtering
make run-processing
```

La idea para tener 3 comandos es que el filtro empiece después de terminado el scrapping. 
