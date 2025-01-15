from .config import RMQ_PASS, RMQ_USER

rabbit_url = f"amqp://{RMQ_USER}:{RMQ_PASS}@localhost:5672/"
