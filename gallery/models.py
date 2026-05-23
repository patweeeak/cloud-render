from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class RecipePhoto(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='recipes/')
    image = CloudinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title