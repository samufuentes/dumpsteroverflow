from django.shortcuts import render

from forms import OverflowForm
from models import Address, Dumpster

def home(request):
    template_name = 'home.html'
    form = OverflowForm()
    context = {'form': form}

    if request.method == 'POST':
        form = OverflowForm(request.POST)
        if form.is_valid():
            print "Form is valid!!"
            # Reset form since we come back to initial view instead of redirect.
            # TODO. Update context: points and point variation
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