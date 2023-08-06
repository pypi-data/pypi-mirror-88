import logging
from logging.handlers import TimedRotatingFileHandler
from kafka import KafkaProducer, KafkaConsumer


class RedisClient(object):
    def __init__(self, hosts, password=None, db=0):
        redis_hosts = self.parse_redis_hosts(hosts)
        if redis_hosts.__len__() is 0:
            self.rclient = None
        elif redis_hosts.__len__() is 1:
            import redis
            self.rclient = redis.StrictRedis(password=password,
                                             db=db,
                                             **redis_hosts[0])
        else:
            import rediscluster
            self.rclient = rediscluster.RedisCluster(password=password, startup_nodes=redis_hosts)

    @staticmethod
    def parse_redis_hosts(hosts):
        redis_hosts = []
        if isinstance(hosts, str):
            hosts = hosts.split(':')
            redis_hosts.append({'host': hosts[0],
                                'port': hosts[1]})
            return redis_hosts

        for host in hosts:
            address = host.split(':')
            redis_hosts.append({'host': address[0],
                                'port': address[1]})

        return redis_hosts

    def set(self, key, value, seconds=None):
        return self.rclient.set(key, value, px=seconds)

    def get(self, key):
        return self.rclient.get(key)

    def hkeys(self, name):
        return self.rclient.hkeys(name)

    def hset(self, name, key, value):
        return self.rclient.hset(name, key, value)

    def hget(self, name, key):
        return self.rclient.hget(name, key)

    def delete(self, key):
        return self.rclient.delete(key)

    def hmset(self, name, mapping):
        return self.rclient.hmset(name, mapping)

    def expire(self, key, time):
        return self.rclient.expire(key, time)



class KafkaClient(object):
    def __init__(self, host, username=None, password=None):
        self.producer = KafkaProducer(bootstrap_servers=host,
                                      sasl_plain_username=username,
                                      sasl_plain_password=password)
        self.consumer = KafkaConsumer(bootstrap_servers=host,
                                      sasl_plain_username=username,
                                      sasl_plain_password=password)

    def send(self, topic, value):
        return self.producer.send(topic=topic, value=value)

    def p_close(self):
        return self.producer.close()

    def subscribe(self, topics):
        return self.consumer.subscribe(topics=topics)

    def poll(self):
        return self.consumer.poll()

    def c_close(self):
        return self.consumer.close()

    def close_all(self):
        self.producer.close()
        self.consumer.close()
        return 0


# log
def log():
    handler = TimedRotatingFileHandler("inference.log", when="D", interval=2, backupCount=5,
                                       encoding="UTF-8", delay=False, utc=True)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    return handler