from django.db import models
from django.contrib.auth.models import User


class GenericFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Address(GenericFieldsMixin):
    street_address = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)

    class Meta:
        unique_together = ('street_address', 'zip_code', 'city')


class Discoverer(GenericFieldsMixin):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)
    default_address = models.OneToOneField(Address)


class Dumpster(GenericFieldsMixin):
    DUMPSTER_TYPES = (
            ('BROWN', 'ORGANIC'),
            ('YELLOW', 'PLASTIC'),
            ('BLUE', 'PAPER'),
            ('GRAY', 'WASTE'),
        )

    dumpster_type = models.CharField(max_length=10, choices=DUMPSTER_TYPES)
    location = models.ForeignKey(Address)
    is_full = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dumpster_type', 'location')


class Overflow(GenericFieldsMixin):
    user = models.ForeignKey(Discoverer)
    dumpster = models.ForeignKey(Dumpster)

