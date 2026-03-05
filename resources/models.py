from django.db import models
from cloudinary.models import CloudinaryField
from curriculum.models import SubStrand, LearningOutcome

class Tag(models.Model):
    name = models.SlugField(max_length=50, unique=True)

    def __str__(self): return self.name

class Material(models.Model):
    MATERIAL_TYPE = (
        ('NOTE', 'Summarized Note'),
        ('REVISION', 'Revision Material'),
        ('SCHEME', 'Scheme of Work'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Brief description of the content")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE, default='NOTE')
    
    substrand = models.ForeignKey(SubStrand, on_delete=models.SET_NULL, null=True, related_name='materials')
    learning_outcomes = models.ManyToManyField(LearningOutcome, blank=True, related_name='materials')
    
    file = CloudinaryField(resource_type='auto') 
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self): return self.title

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return ""