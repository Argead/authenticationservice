import redis
import json
from key_generator import APIKeyGenerator

class RedisQueueManager:
    def __init__(self):
        self.r = redis.Redis(host="redis-server", port=6379)

    def push_to_queue(self, api_key, identifier):
        data = self._jsonify_key(api_key, identifier)
        r.rpush("queue:keys", data)

    def _jsonify_key(api_key, identifier):
        data = {
            "api_key": api_key,
            "identifier": identifier
        }
        return json.dumps(data)

    def _get_new_key():
        return
