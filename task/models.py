from django.db import models
from django.core.validators import MinLengthValidator

class Categorie(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    priority_choice = [
        ('Basse', 'Basse'),
        ('Moyenne', 'Moyenne'),
        ('Haute', 'Haute'),
        ('Maximale', 'Maximale'),
    ]
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=priority_choice, default='Basse')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['categorie', 'end_date', 'start_date', 'priority'])
        ]
