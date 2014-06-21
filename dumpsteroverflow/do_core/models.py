from django.db import models
from django.contrib.auth.models import User

class GenericFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Discoverer(GenericFieldsMixin):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)

class Address(GenericFieldsMixin):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)

class Dumpster(GenericFieldsMixin):
    DUMPSTER_TYPES = (
            ('BROWN', 'ORGANIC'),
            ('YELLOW', 'PLASTIC'),
            ('BLUE', 'PAPER'),
            ('GRAY', 'WASTE'),
        )

    dumpster_type = models.CharField(max_length=1, choices=DUMPSTER_TYPES)
    location = models.ForeignKey(Address)

class Overflow(GenericFieldsMixin):
    user = models.ForeignKey(Discoverer)
    dumpster = models.ForeignKey(Dumpster)

