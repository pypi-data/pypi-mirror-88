# -*- coding: utf-8 -*-
import os
import json

env_dist = os.environ
# async message storage by kafka
if 'status_provider' in env_dist:
    status_kafka = env_dist['status_provider']
    if status_kafka is None:
        print('Kafka status_provider does not exist!')
    else:
        status_kafka = json.loads(status_kafka)
        KAFKA_HOST = status_kafka['address'] if 'address' in status_kafka.keys() else None
        KAFKA_USERNAME = status_kafka['username'] if 'username' in status_kafka.keys() else None
        KAFKA_PASSWORD = status_kafka['password'] if 'password' in status_kafka.keys() else None
        KAFKA_TOPIC_STOP = status_kafka['topic'] if 'topic' in status_kafka.keys() else None
# data storage in Redis, the form of redis hosts and password like follow
# hosts = '10.70.151.183:6379' or
# ['10.70.151.183:6379', '10.70.151.225:6379', '10.70.151.205:6379',
# '10.70.151.232:6379', '10.70.151.239:6379', '10.70.151.231:6379']
# password = 'xxxxxxx'
if 'src_provider' in env_dist:
    src_redis = env_dist['src_provider']
    src_redis = json.loads(src_redis)
    SRC_REDIS_HOSTS = src_redis['address']
    SRC_REDIS_PASSWORD = src_redis['password'] if 'password' in src_redis.keys() else None
    SRC_REDIS_DB = src_redis['database'] if 'database' in src_redis.keys() else 0
    SRC_BATCH_ID = src_redis['batch_id']
if 'dst_provider' in env_dist:
    dst_redis = env_dist['dst_provider']
    dst_redis = json.loads(dst_redis)
    DST_REDIS_HOSTS = dst_redis['address']
    DST_REDIS_PASSWORD = dst_redis['password'] if 'password' in dst_redis.keys() else None
    DST_REDIS_DB = dst_redis['database'] if 'database' in dst_redis.keys() else 0
    RESULT_KEY = dst_redis['result_key']
    PROGRESS_KEY = dst_redis['progress_key']

if 'inference_type' in env_dist:
    INFERENCE_TYPE = env_dist['inference_type']
# DEBUG FINAL VALUES
DEBUG_INFER_RLT_REDIS = {"redis_host": "10.73.1.31:32730", "password": "ai13579", "db": "3"}
DEBUG_SRC_REDIS_DICT = {"redis_host": "10.73.1.31:32730", "password": "ai13579", "db": "1"}
ENGINE_MODULE_PATH = 'sdk.inference'
ENGINE_CLASS_NAME = 'Engine'
LOAD_MODEL_METHOD_NAME = 'load_model'
INFERENCE_METHOD_NAME = 'inference'
RELEASE_GPU_RES_METHOD_NAME = 'release_gpu_res'