# --- manager/admin.py ---
from django.contrib import admin
from .models import ShiftSlot

@admin.register(ShiftSlot)
class ShiftSlotAdmin(admin.ModelAdmin):
    list_display = ("date", "time_slot", "capacity", "remaining", "is_available")
    list_filter = ("date", "is_available")
    ordering = ("date", "time_slot")
