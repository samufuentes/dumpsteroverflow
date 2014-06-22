from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from forms import OverflowForm
from models import Address, Dumpster
from django.views.generic.base import View
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
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
        print "Hola, ", user
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
    context = {'form': form}

    if request.method == 'POST':
        form = OverflowForm(request.POST)
        if form.is_valid():
            points = 0
            address, created = Address.objects.get_or_create(street_address=form.cleaned_data['street_address'],
                zip_code=form.cleaned_data['zip_code'], city=form.cleaned_data['city'])
            for field, dumpster_type in Dumpster.DUMPSTER_FIELDS.items():
                if form.cleaned_data[field]:
                    dumpster, created = Dumpster.objects.get_or_create(dumpster_type=dumpster_type, location=address)
                    dumpster.is_full = True
                    dumpster.dumpster_type = dumpster_type
                    dumpster.save()
                    points += 3

            return HttpResponseRedirect(reverse('overflow', args=(points,)))
    else:
        address = request.user.discoverer.default_address
        if address:
            form.city = address.city
            form.zip_code = address.zip_code
            form.street_address = address.street_address
            context = {'form': form}

    return render(request, template_name, context)

def overflow(request, points):
    if points=='0':
        return render(request, 'overflow_sent.html', {'flash_error': 'This dumpster overflow was already reported.'})
    else:
        return render(request, 'overflow_sent.html', {'points': points})
