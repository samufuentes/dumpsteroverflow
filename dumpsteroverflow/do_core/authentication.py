from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from dumpsteroverflow.do_core.models import Address, Discoverer
import paypalrestsdk as pp


class PaypalBackend(ModelBackend):
    def authenticate(self, token=None):
        tokeninfo = pp.Tokeninfo.create(token)
        if tokeninfo is None:
            return
        userinfo = tokeninfo.userinfo()
        email = userinfo['email']
        user, user_created = User.objects.get_or_create(
            username=email)
        discoverer, discoverer_created = Discoverer.objects.get_or_create(
            user=user)
        if user_created:
            user.email = email
            user.first_name = userinfo['given_name']
            user.last_name = userinfo['family_name']
            user.save()
        if discoverer_created:
            address = userinfo['address']
            discoverer.default_address = Address.objects.get_or_create(
                street_address=address['street_address'],
                zip_code=address['postal_code'],
                city=address['locality'])
            discoverer.save()
