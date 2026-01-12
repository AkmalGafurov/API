from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)


    def __str__(self):
        if self.parent:
            return f"{self.parent.title} {self.title}"
        return self.title
    
    class Meta:
        verbose_name_plural = 'catigories'
    