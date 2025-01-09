from django.shortcuts import render
from major.forms import * 
from django.contrib import messages
# Create your views here.

def BreederView(request):
    if request.method == "POST":
        breeder_form = Breeder_Form(request.POST)
        if breeder_form.is_valid():
            breeder_form.save()

    else :
        breeder_form = Breeder_Form()
    return render(request, 'home_page.html', {'form': breeder_form})


def front(request):
    return render(request, "frontpage.html")