import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class DriverService:
    name = "driver_service"

    redis = Redis("development")

    @rpc
    def get(self, driver_id):
        driver = self.redis.get(driver_id)
        return driver

    @rpc
    def create(self, driver_name):
        driver_id = str(uuid.uuid4())
        self.redis.set(driver_id, driver_name)
        return driver_id
