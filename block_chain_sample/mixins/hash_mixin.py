import hashlib
import json as ujson


class HashMixin:
    def hash(self, hash_func=hashlib.sha256):
        return hash_func(ujson.dumps(self._asdict(), sort_keys=True).encode("utf-8")).hexdigest()
