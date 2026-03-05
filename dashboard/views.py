from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from resources.models import Material

@login_required
def teacher_dashboard(request):
    # Get all materials, with related data to avoid extra queries
    materials = Material.objects.select_related('substrand').all().order_by('-uploaded_at')
    
    context = {
        'materials': materials
    }
    return render(request, 'dashboard/teacher_home.html', context)