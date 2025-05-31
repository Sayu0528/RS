from django.db import models

# Create your models here.

TIME_SLOT_CHOICES = [
    ("8:00〜9:00", "8:00〜9:00"),
    ("9:00〜10:30", "9:00〜10:30"),
    ("10:40〜12:10", "10:40〜12:10"),
    ("12:10〜13:00", "12:10〜13:00"),
    ("13:00〜14:30","13:00〜14:30"),
    ("14:45〜16:15","14:45〜16:15"),
    ("16:30〜18:00","16:30〜18:00"),
    ("18:15〜19:45","18:15〜19:45")
]

class ShiftSlot(models.Model):
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES)
    capacity = models.PositiveSmallIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("date", "time_slot")
        ordering = ["date", "time_slot"]



    def __str__(self):
        return f"{self.date} {self.time_slot}"
    
    @property
    def remaining(self) -> int:
        """残り予約可能人数"""
        return max(self.capacity - self.reservations.count(), 0)

    def update_availability(self):
        """残枠に応じて is_available を自動更新"""
        new_flag = self.remaining > 0
        if new_flag != self.is_available:
            self.is_available = new_flag
            self.save(update_fields=["is_available"])  # 無限ループ防止
