# student/models.py

from django.db import models
from manager.models import ShiftSlot
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Reservation(models.Model):
    shift_slot = models.ForeignKey(
        ShiftSlot,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    student_name = models.CharField("氏名", max_length=100)
    student_id = models.CharField("学籍番号", max_length=20)
    student_email = models.EmailField("メールアドレス")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # ← ここをクラス内にインデント
        unique_together = ("shift_slot", "student_id")
        ordering = ["-created_at"]

    def __str__(self):  # ← これもクラス内にインデント
        return f"{self.student_name} → {self.shift_slot}"

# ── signals ──
@receiver([post_save, post_delete], sender=Reservation)
def refresh_slot_availability(sender, instance, **kwargs):
    instance.shift_slot.update_availability()
