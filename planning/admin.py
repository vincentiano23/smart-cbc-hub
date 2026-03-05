from django.contrib import admin
from .models import LessonPlan

@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'substrand', 'status', 'created_at')
    readonly_fields = ('content',) # Make the JSON read-only in admin to avoid breaking format