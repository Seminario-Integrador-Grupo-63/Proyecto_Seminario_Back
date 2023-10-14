import pickle
import redis


class RedisService:
    redis_client = redis.Redis(host="redis", port=6379)

    @classmethod
    def save_set(self, key: str, data):
        stored_data = self.redis_client.get(key)
        if stored_data:
            stored_data = pickle.loads(stored_data)
        else:
            stored_data = set() 
        
        if data in stored_data:
            saved = False
        else:
            saved = True
            stored_data.add(data)

            encoded_data = pickle.dumps(stored_data)

            self.redis_client.set(key, encoded_data)

        return stored_data, saved
    
    @classmethod
    def save_list(self, key:str, data: any, time:int | None = None):
        stored_data = self.redis_client.get(key)
        if stored_data:
            stored_data = pickle.loads(stored_data)
        else:
            stored_data = [] 
        
        stored_data.append(data)

        encoded_data = pickle.dumps(stored_data)

        self.redis_client.set(key, encoded_data, time) if time else self.redis_client.set(key, encoded_data)

        return stored_data

    @classmethod
    def get_data(self, key:str):
        data = self.redis_client.get(key)
        if data:
            return pickle.loads(data)
        else:
            return None
    
    @classmethod
    def delete_data(self, key: str):
        self.redis_client.delete(key)
    
    @classmethod
    def remove_from_list(self, key:str, data):
        stored_data = self.redis_client.get(key)
        stored_data: list = pickle.loads(stored_data)
        stored_data.remove(data)
        encoded_data = pickle.dumps(stored_data)

        self.redis_client.set(key, encoded_data)

        return stored_data

redis_service = RedisService()
