import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class PassengerService:
    name = "passenger_service"

    redis = Redis("development")

    @rpc
    def get(self, passenger_id):
        passenger = self.redis.get(passenger_id)
        return passenger

    @rpc
    def create(self, passenger_name):
        passenger_id = int(uuid.uuid4())
        self.redis.set(passenger_id, passenger_name)
        return passenger_id
