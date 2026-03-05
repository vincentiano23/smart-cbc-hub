from django.contrib import admin
from .models import Material, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'substrand', 'uploaded_at')
    list_filter = ('material_type', 'uploaded_at', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('learning_outcomes', 'tags') # Nice widget for selection
    
    # Optimization: fetch related objects to reduce database queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('substrand')