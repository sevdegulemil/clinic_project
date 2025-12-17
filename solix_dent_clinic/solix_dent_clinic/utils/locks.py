import uuid
import redis
from django.conf import settings
from django.db import transaction, connection

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def lock_slot(slot_id, ttl=10):
    """
    Slot için lock almaya çalışır.
    Redis varsa Redis kullanır,
    Redis yoksa DB lock'a düşer.
    """

    lock_key = f"slot:{slot_id}"
    lock_value = str(uuid.uuid4())

    try:

        locked = r.set(lock_key, lock_value, nx=True, ex=ttl)

        if not locked:
            return False

        return lock_key, lock_value

    except Exception:
        
        return "db", slot_id


def unlock_slot(lock_result):
    """
    Redis lock açma
    """
    if not lock_result:
        return

    if lock_result == "db":
        return

    lock_key, lock_value = lock_result

    try:
        current = r.get(lock_key)
        if current == lock_value:
            r.delete(lock_key)
    except Exception:
        pass


def db_lock_slot(slot_id):
    """
    DB fallback lock
    """
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM doctor_slot WHERE id = %s FOR UPDATE",
                [slot_id]
            )
        return True
