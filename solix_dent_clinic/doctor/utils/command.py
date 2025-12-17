from django.utils import timezone
from doctor.models import WaitingList
from doctor.views import handle_slot_freed


def check_expired_waiting_lists():
    """
    NOTIFIED olan waiting list kayıtlarını kontrol eder.
    30 dk süresi dolanları EXPIRED yapar
    ve sıradaki kullanıcıya geçer.
    """

    notified_items = WaitingList.objects.filter(status="NOTIFIED")

    for item in notified_items:
        # 30 dk dolmuş mu?
        if item.notified_at is None:
            continue

        time_diff = timezone.now() - item.notified_at

        if time_diff.total_seconds() >= 30 * 60:
            item.status = "EXPIRED"
            item.save()

            # Aynı slot için sıradaki kişiye geç
            handle_slot_freed(item.slot)
