from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from forms import OverflowForm
from models import Address, Dumpster
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import paypalrestsdk as pp
import os


def login(request):
    token = request.GET.get('code')
    status = request.GET.get('next') or request.GET.get('status')
    pp.configure({
        "mode": os.environ['PAYPAL_MODE'],
        "client_id": os.environ['PAYPAL_CLIENT_ID'],
        "client_secret": os.environ['PAYPAL_CLIENT_SECRET'],
        "openid_redirect_uri": os.environ['PAYPAL_OPENID_REDIRECT_URI']})
    if token:
        user = authenticate(token=token)
        if user is not None:
            login(request, user)
        redirect_url = status
    else:
        redirect_url = pp.Tokeninfo.authorize_url({
            "scope": "profile email address phone https://uri.paypal.com/services/paypalattributes",
            "state": str(status)})
    return redirect(redirect_url)


@login_required(login_url='login/')
def home(request):
    template_name = 'home.html'
    form = OverflowForm()
    context = {'form': form}

    if request.method == 'POST':
        form = OverflowForm(request.POST)
        if form.is_valid():
            # Reset form since we come back to initial view instead of redirect.
            # TODO. Update context: points and point variation
            points = 0
            address, created = Address.objects.get_or_create(street_address=form.cleaned_data['street_address'],
                zip_code=form.cleaned_data['zip_code'], city=form.cleaned_data['city'])
            if form.cleaned_data['is_brown']:
                dumpster, created = Dumpster.objects.get_or_create(dumpster_type=Dumpster.DUMPSTER_TYPES[0], location=address)
                if not dumpster.is_full:
                    dumpster.is_full = True
                    dumpster.save()
                    # TODO: Update points
                    points = 3
                    # TODO: Send alert to garbage collectors
                else:
                    points = 0

            return HttpResponseRedirect(reverse('overflow', args=(points,)))
    return render(request, template_name, context)

def overflow(request, points):
    if points=='0':
        return render(request, 'overflow_sent.html', {'flash_error': 'This dumpster overflow was already reported.'})
    else:
        return render(request, 'overflow_sent.html', {'points': points})
            # address = Address.objects.get_or_create(street_address=form.cleaned_data['street_address'],
            #     zip_code=form.cleaned_data['zip_code'], city=form.cleaned_data['city'])
            # if form.cleaned_data['is_brown']:
            #     dumpster = Dumpster.objects.get_or_create(dumpster_type=Dumpster.DUMPSTER_TYPE[0], location=address)
            #     if not dumpster.is_full:
            #         dumpster.is_full = True
            #         dumpster.save()
            #         # TODO: Update points
            #         # TODO: Send alert to garbage collectors
        form = OverflowForm()
    return render(request, template_name, context)
