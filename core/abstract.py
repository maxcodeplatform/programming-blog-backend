from django.db import models


class BaseModel(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    write_at = models.DateTimeField(auto_now=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
