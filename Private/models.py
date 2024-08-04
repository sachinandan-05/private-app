import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class PrivateModel(models.Model):
    title = models.CharField(max_length=300, default='')
    date_name = models.DateField()
    private_description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    share = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.date_name} - {self.user}'


class Private_SubModel(models.Model):
    private_id = models.ForeignKey(PrivateModel, on_delete=models.CASCADE, null=True)
    private_img = models.FileField(null=True, upload_to='Private/PrivateImage')
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Delete the images/videos file when the product is deleted
        os.remove(self.private_img.path)
        super(Private_SubModel, self).delete(*args, **kwargs)

    def __str__(self):
        return "%s" % self.private_id


# Delete the images/videos file
@receiver(pre_delete, sender=PrivateModel)
def delete_subcategory_images(sender, instance, **kwargs):
    subcategories = Private_SubModel.objects.filter(private_id=instance)

    # Delete subcategory images
    for subcategory in subcategories:
        image_path = os.path.join(settings.MEDIA_ROOT, str(subcategory.private_img))
        if os.path.exists(image_path):
            os.remove(image_path)
