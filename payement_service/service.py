import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class PaymentService:
    name = "payment_service"
