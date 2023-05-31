from django.db import models


# Create your models here.

class Blog_post(models.Model):
    title = models.CharField(max_length=255)
    post_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    head0 = models.CharField(max_length=500, default="")
    contenthead0 = models.CharField(max_length=500, default="")
    head1 = models.CharField(max_length=500, default="")
    contenthead1 = models.CharField(max_length=500, default="")
    head2 = models.CharField(max_length=500, default="")
    contenthead2 = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to="shop/images", default="image")

    def __str__(self):
        return self.title
