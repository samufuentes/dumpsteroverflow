from django.views.generic.edit import FormView
from forms import OverflowForm
from models import Address, Dumpster

class HomeView(FormView):
    template_name = 'home.html'
    form_class = OverflowForm
    success_url = '/'

    def form_valid(self, form):
        address = Address.objects.get_or_create(street_address=form.cleaned_data['street_address'],
            zip_code=form.cleaned_data['zip_code'], city=form.cleaned_data['city'])
        if form.cleaned_data['is_brown']:
            dumpster = Dumpster.objects.get_or_create(dumpster_type=Dumpster.DUMPSTER_TYPE[0], location=address)
            if not dumpster.is_full:
                dumpster.is_full = True
                # TODO: Update points
                # TODO: Send alert to garbage collectors
        return super(HomeView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     # Change context here
    #     return context
