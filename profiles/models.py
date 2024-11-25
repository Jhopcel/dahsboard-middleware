from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Business_sector(models.Model):
    id = models.AutoField(primary_key=True)
    name_sector = models.CharField(max_length=50)

    def __str__(self):
        return self.name_sector

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='photos')
    bio = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    sector = models.ForeignKey(Business_sector, on_delete=models.CASCADE, default=None)
    id_unique = models.CharField(max_length=10, unique=True, default=generate_random_id)

    def __str__(self):
        return f"Profile of {self.user.username}"

    # Aquí podrías agregar un método para asegurarte de que el ID único sea siempre generado correctamente.
    def save(self, *args, **kwargs):
        # Si no se ha asignado un ID único, lo generamos automáticamente
        if not self.id_unique:
            self.id_unique = generate_random_id()
        super().save(*args, **kwargs)