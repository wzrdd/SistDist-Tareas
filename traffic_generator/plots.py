import json
import matplotlib.pyplot as plt

# Archivos generados
archivos = ['poisson_lru.json', 'poisson_lfu.json', 'pareto_lru.json', 'pareto_lfu.json']

labels = []
hits = []
misses = []
evictions = []

# Cargar los datos
for archivo in archivos:
    with open(archivo, 'r') as f:
        data = json.load(f)
        labels.append(f"{data['distribution']}_{data['eviction_policy'].replace('allkeys-', '')}")
        hits.append(data['hits'])
        misses.append(data['misses'])
        evictions.append(data['evictions'])

# Crear gráfico
x = range(len(labels))

plt.figure(figsize=(10, 6))
plt.bar(x, hits, width=0.25, label='Hits', align='center')
plt.bar([i + 0.25 for i in x], misses, width=0.25, label='Misses', align='center')
plt.bar([i + 0.5 for i in x], evictions, width=0.25, label='Evictions', align='center')

plt.xlabel('Configuraciones')
plt.ylabel('Cantidad')
plt.title('Comparación de Métricas por Configuración')
plt.xticks([i + 0.25 for i in x], labels, rotation=15)
plt.legend()
plt.tight_layout()
plt.grid(axis='y')
plt.savefig('metricas_comparadas.png')
plt.close()
