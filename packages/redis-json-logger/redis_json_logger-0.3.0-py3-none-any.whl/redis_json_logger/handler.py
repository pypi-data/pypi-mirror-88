import logging
import redis


class RedisLogHandler(logging.Handler):

    def __init__(self, key="log-key-redis", host='localhost'):
        logging.Handler.__init__(self)
        self.key = key
        self.redis_server = redis.Redis(host)

    def get_key(self, record: logging.LogRecord):
        try:
            return record.name  # using logger name as `redis key`
        except AttributeError:
            return self.key

    def emit(self, record):
        try:
            self.redis_server.rpush(self.get_key(record), self.format(record))
        except:  # noqa
            pass
