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

    def __unicode__(self):
        return u'%s %d %s' %(self.street_address, self.zip_code, self.city)


class Discoverer(GenericFieldsMixin):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)
    default_address = models.OneToOneField(Address, null=True)

    def __unicode__(self):
        return u'%s' %self.user.__unicode__()


class Dumpster(GenericFieldsMixin):
    DUMPSTER_TYPES = (
            ('BROWN', 'ORGANIC'),
            ('YELLOW', 'PLASTIC'),
            ('BLUE', 'PAPER'),
            ('GRAY', 'WASTE'),
        )
    DUMPSTER_FIELDS = {
        'is_brown': DUMPSTER_TYPES[0][0],
        'is_yellow': DUMPSTER_TYPES[1][0],
        'is_blue': DUMPSTER_TYPES[2][0],
        'is_gray': DUMPSTER_TYPES[3][0]
    }

    dumpster_type = models.CharField(max_length=10, choices=DUMPSTER_TYPES)
    location = models.ForeignKey(Address)
    is_full = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dumpster_type', 'location')

    def __unicode__(self):
        return u'%s %s' %(self.dumpster_type, self.location.__unicode__())


class Overflow(GenericFieldsMixin):
    user = models.ForeignKey(Discoverer)
    dumpster = models.ForeignKey(Dumpster)

