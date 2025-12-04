from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from major.forms import *
from django.contrib import messages

# Class-based views
class BreederCreateView(FormView):
    template_name = 'breed_form.html'
    form_class = Breeder_Form

    def form_valid(self, form):
        form.save()
        return render(self.request, self.template_name, {'form': self.form_class()})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class FrontpageView(TemplateView):
    template_name = 'frontpage.html'
