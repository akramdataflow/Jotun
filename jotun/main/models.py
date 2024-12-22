from django.db import models

# Create your models here.

def image_upload(instance, filename):
    imagename, extension = filename.split('.')
    return "product/%s.%s" % (instance.id, extension)

class Category(models.Model):
    title = models.CharField(max_length=3000)

    def __str__(self):
        return self.title

class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return self.name


