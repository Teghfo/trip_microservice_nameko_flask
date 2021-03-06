import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class TripService:
    name = "trip_service"

    redis = Redis("development")

    @rpc
    def get(self, trip_id):
        trip_data = self.redis.hgetall(trip_id)
        return trip_data

    @rpc
    def create(self, passenger_id, driver_id, from_loc, to_loc):
        trip_id = str(uuid.uuid4())
        self.redis.hmset(trip_id, {
            "passenger_id": passenger_id,
            "driver_id": driver_id,
            "from_loc": from_loc,
            "to_loc": to_loc
        })
        return trip_id
