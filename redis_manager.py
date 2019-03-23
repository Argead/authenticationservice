import redis
import json
from key_generator import APIKeyGenerator

class RedisQueueManager:
    def __init__(self):
        self.r = redis.Redis(host="redis-server", port=6379)

    def push_keys_to_queue(self):
        api_key, identifier = self._get_new_key()
        data = self._jsonify_key(api_key, identifier)
        r.rpush("queue:keys", data)
        return True

    def fill_queue(self):
        if self.r.llen() < 10:
            self.push_keys_to_queue()
            self.fill_queue()

    def _jsonify_key(api_key, identifier):
        data = {
            "api_key": api_key,
            "identifier": identifier
        }
        return json.dumps(data)

    def _get_new_key():
        gen = APIKeyGenerator()
        return gen.create_key_pair()


if __name__ == "__main__":
    q = RedisQueueManager()
    q.fill_queue()
