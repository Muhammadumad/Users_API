import uuid
from django.db import models


class User(models.Model):
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age   = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} ({self.email})"