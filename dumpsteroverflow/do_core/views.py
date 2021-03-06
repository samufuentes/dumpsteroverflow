from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from forms import OverflowForm
from models import Address, Dumpster, Overflow
from django.views.generic.base import View
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from geopy.geocoders import GoogleV3
import json
import paypalrestsdk as pp
import os


def login(request):
    token = request.GET.get('code')
    pp.configure({
        "mode": os.environ['PAYPAL_MODE'],
        "client_id": os.environ['PAYPAL_CLIENT_ID'],
        "client_secret": os.environ['PAYPAL_CLIENT_SECRET'],
        "openid_redirect_uri": os.environ['PAYPAL_OPENID_REDIRECT_URI']})
    if token:
        user = authenticate(token=token)
        if user is not None:
            auth_login(request, user)
            redirect_url = '/'
    else:
        redirect_url = pp.Tokeninfo.authorize_url({
            "scope": "profile email address phone https://uri.paypal.com/services/paypalattributes",
            })
    return redirect(redirect_url)


@login_required(login_url='login/', redirect_field_name='status')
def home(request):
    template_name = 'home.html'
    form = OverflowForm()

    if request.method == 'POST':
        form = OverflowForm(request.POST)
        if form.is_valid():
            points = 0
            address, created = Address.objects.get_or_create(street_address=form.cleaned_data['street_address'],
                zip_code=form.cleaned_data['zip_code'], city=form.cleaned_data['city'])
            for field, dumpster_type in Dumpster.DUMPSTER_FIELDS.items():
                if form.cleaned_data[field]:
                    dumpster, created = Dumpster.objects.get_or_create(dumpster_type=dumpster_type, location=address)
                    dumpster.dumpster_type = dumpster_type
                    if not dumpster.is_full:
                        dumpster.is_full = True
                        points += 3
                        Overflow.objects.create(user=request.user.discoverer, dumpster=dumpster)
                    dumpster.save()
            request.user.discoverer.points += points
            request.user.discoverer.save()
            return HttpResponseRedirect(reverse('overflow', args=(points,)))
    else:
        address = request.user.discoverer.default_address
        if address:
            formdict = {'city': address.city,
                        'zip_code': address.zip_code,
                        'street_address': address.street_address}
            form = OverflowForm(initial=formdict)

    context = {'form': form}
    return render(request, template_name, context)

def overflow(request, points):
    if points=='0':
        return render(request, 'overflow_sent.html', {'flash_error': 'This dumpster overflow was already reported.'})
    else:
        return render(request, 'overflow_sent.html', {'points': points})

def geo(request):
    lat = request.POST['lat']
    lng = request.POST['lng']
    geolocator = GoogleV3()
    location = geolocator.reverse("{}, {}".format(lat, lng))
    json_data = json.dumps(location.raw)
    return HttpResponse(json_data, mimetype="application/json")
