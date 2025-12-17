import uuid
from doctor.models import IdempotentRequest

def check_idempotency(user, action):
    """
    Aynı kullanıcı aynı action'ı daha önce yaptı mı?
    """
    key = f"{user.id}:{action}"

    exists = IdempotentRequest.objects.filter(
        key=key
    ).exists()

    if exists:
        return False

    IdempotentRequest.objects.create(
        user=user,
        action=action,
        key=key
    )
    return True
