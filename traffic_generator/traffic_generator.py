import time
import random
import json
from pymongo import MongoClient
import numpy as np
import redis
import os
from bson import ObjectId
from dotenv import load_dotenv
import datetime

load_dotenv()

client = MongoClient("mongodb://dumbuser:dumbpassword@mongo:27017")
db = client["admin"]
alerts_collection = db["alerts"]

distribution = os.getenv('DISTRIBUTION', 'poisson').lower()
eviction_policy = os.getenv('EVICTION_POLICY', 'allkeys-lru').lower()

redis_hosts = {
    ('poisson', 'allkeys-lru'): 'redis_poisson_lru',
    ('poisson', 'allkeys-lfu'): 'redis_poisson_lfu',
    ('pareto', 'allkeys-lru'): 'redis_pareto_lru',
    ('pareto', 'allkeys-lfu'): 'redis_pareto_lfu',
}

redis_host = redis_hosts.get((distribution, eviction_policy))
print(f"[INFO] Conectando a Redis host: {redis_host}")
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

# Globales para métricas
total_queries_realizadas = 0
tiempo_total_generacion = 0

def default_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def cache_event(event):
    event_id = event['_id']
    event_data = json.dumps(event, default=default_serializer)
    try:
        redis_client.set(f"event_cache:{event_id}", event_data)
    except redis.exceptions.ResponseError as e:
        print(f"[ERROR] Redis no pudo guardar {event_id}: {e}")

def is_event_cached(event_id):
    return redis_client.exists(f"event_cache:{event_id}")

def obtener_evento_random():
    pipeline = [{"$sample": {"size": 1}}]
    result = list(alerts_collection.aggregate(pipeline))
    if result:
        return result[0]
    print("[WARN] No se pudo obtener evento aleatorio (pipeline vacío).")
    return None

def generador_poisson(lam, num_consultas):
    global total_queries_realizadas, tiempo_total_generacion
    print(f"[START] Generando {num_consultas} eventos con distribución Poisson...")
    tiempos = np.random.poisson(lam, num_consultas)

    start_time = time.time()
    for i, t in enumerate(tiempos):
        time.sleep(max(t / 10000, 0.00005))
        evento = obtener_evento_random()
        if evento:
            if not is_event_cached(evento['_id']):
                cache_event(evento)
            total_queries_realizadas += 1
            if total_queries_realizadas % 1000 == 0:
                print(f"[POISSON] Progreso: {total_queries_realizadas}/{num_consultas} consultas")
    end_time = time.time()
    tiempo_total_generacion = end_time - start_time
    print(f"[DONE] Poisson terminado. Consultas: {total_queries_realizadas}")

def generador_pareto(shape, num_consultas):
    global total_queries_realizadas, tiempo_total_generacion
    print(f"[START] Generando {num_consultas} eventos con distribución Pareto...")
    tiempos = np.random.pareto(shape, num_consultas)

    start_time = time.time()
    for i, t in enumerate(tiempos):
        time.sleep(max(t / 10000, 0.00005))
        evento = obtener_evento_random()
        if evento:
            if not is_event_cached(evento['_id']):
                cache_event(evento)
            total_queries_realizadas += 1
            if total_queries_realizadas % 1000 == 0:
                print(f"[PARETO] Progreso: {total_queries_realizadas}/{num_consultas} consultas")
    end_time = time.time()
    tiempo_total_generacion = end_time - start_time
    print(f"[DONE] Pareto terminado. Consultas: {total_queries_realizadas}")

def imprimir_metricas():
    stats = redis_client.info('stats')
    hits = stats.get('keyspace_hits', 0)
    misses = stats.get('keyspace_misses', 0)
    evictions = stats.get('evicted_keys', 0)

    memory_info = redis_client.info('memory')
    used_memory_bytes = memory_info.get('used_memory', 0)
    used_memory_mb = used_memory_bytes / (1024 * 1024) if used_memory_bytes else 0


    tiempo_promedio = tiempo_total_generacion / total_queries_realizadas if total_queries_realizadas > 0 else 0

    metricas = {
        "timestamp": datetime.datetime.now().isoformat(),
        "distribution": distribution,
        "eviction_policy": eviction_policy,
        "hits": hits,
        "misses": misses,
        "evictions": evictions,
        "queries_realizadas": total_queries_realizadas,
        "total_time_seconds": tiempo_total_generacion,
        "avg_time_per_query_seconds": tiempo_promedio,
        "used_memory_mb": f"{used_memory_mb:.2f}"
    }

    dist = distribution
    policy = eviction_policy.replace('allkeys-', '')
    filename = f"{dist}_{policy}.json"

    with open(filename, 'w') as f:
        json.dump(metricas, f, indent=4)

    print(f"[METRICAS] Guardadas en {filename}")

def main():
    print(f"[INIT] DISTRIBUTION={distribution} | EVICTION_POLICY={eviction_policy}")
    time.sleep(10)
    if distribution == 'poisson':
        generador_poisson(lam=5, num_consultas=50000)
    elif distribution == 'pareto':
        generador_pareto(shape=2, num_consultas=50000)
    else:
        print(f"[ERROR] Distribución no reconocida: {distribution}")

    imprimir_metricas()

if __name__ == "__main__":
    main()
