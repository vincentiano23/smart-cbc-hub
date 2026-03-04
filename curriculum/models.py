from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Grade 4", "Grade 5"
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['id']

    def __str__(self): return self.name


class LearningArea(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Mathematics", "Agriculture"
    code = models.CharField(max_length=10, unique=True) # e.g., "MATH", "AGR"
    grades = models.ManyToManyField(Grade, related_name='learning_areas')

    class Meta:
        verbose_name = "Learning Area"
        verbose_name_plural = "Learning Areas"

    def __str__(self): return f"{self.code} - {self.name}"


class Strand(models.Model):
    learning_area = models.ForeignKey(LearningArea, on_delete=models.CASCADE, related_name='strands')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self): return f"{self.learning_area.code}: {self.name}"


class SubStrand(models.Model):
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='substrands')
    name = models.CharField(max_length=200)
    suggested_duration = models.PositiveIntegerField(help_text="Duration in hours", default=1)

    def __str__(self): return self.name


class LearningOutcome(models.Model):
    """
    Specific Learning Outcome (SLO)
    """
    substrand = models.ForeignKey(SubStrand, on_delete=models.CASCADE, related_name='outcomes')
    code = models.CharField(max_length=50, help_text="e.g. 4.1.1") # CBC codes are specific
    description = models.TextField()

    def __str__(self): return f"{self.code}: {self.description[:50]}..."