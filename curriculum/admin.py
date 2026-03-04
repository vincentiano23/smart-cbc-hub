from django.contrib import admin
from .models import Grade, LearningArea, Strand, SubStrand, LearningOutcome

# Use @admin.register decorator for cleaner code
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(LearningArea)
class LearningAreaAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    filter_horizontal = ('grades',) # Nice widget for ManyToMany

@admin.register(Strand)
class StrandAdmin(admin.ModelAdmin):
    list_display = ('learning_area', 'grade', 'name', 'order')
    list_filter = ('grade', 'learning_area')

@admin.register(SubStrand)
class SubStrandAdmin(admin.ModelAdmin):
    list_display = ('strand', 'name', 'suggested_duration')

@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('code', 'substrand', 'description_short')
    list_filter = ('substrand__strand__learning_area',)
    search_fields = ('code', 'description')

    def description_short(self, obj):
        return obj.description[:50] + "..."
    description_short.short_description = "Description"