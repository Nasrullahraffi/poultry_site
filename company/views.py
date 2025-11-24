from django.shortcuts import render, HttpResponseRedirect
from django.views import View   
from company.forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth import authenticate


# Create your views here.

def companyView(request):
    if request.method == "POST":
        form = Company_Form(request.POST)
        if form.is_valid :
            form.save()
    else :
        form = Company_Form()
    return render(request, 'company/company.html', {"form": form})


class CompanyRegView(View):
    def get(self, request):
         form = CompanyRegForm()
         return render (request, 'company/CompanyReg.html', {'form':form})

    def post(self, request):
        form = CompanyRegForm(request.POST)
        if form.is_valid() :
            messages.success(request, 'Congratulations!! registered Successfully')
            form.save()
            form = CompanyRegForm()
            success_url = '/'
        return render (request, 'company/CompanyReg.html', {'form':form})




# @login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('accounts/login')