from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View

from forms import OverflowForm
from models import Address, Dumpster

def home(request):
    template_name = 'home.html'
    form = OverflowForm()
    context = {'form': form}

    if request.method == 'POST':
        form = OverflowForm(request.POST)
        if form.is_valid():
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
    print form
    return render(request, template_name, context)
