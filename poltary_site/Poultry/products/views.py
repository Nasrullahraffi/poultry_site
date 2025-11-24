from django.shortcuts import render
from products.forms import *
from django.contrib import messages
from products.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@login_required
def MedicineView(request):
    medicine_form = Medicine_Model.objects.all()
    return render(request, 'products/medicine.html', {'medicine_form': medicine_form})

@login_required
def FeedView(request):
    feed_form = Feed_Model.objects.all()
    return render(request, 'products/feed.html', {'feed_form': feed_form})

@login_required
def ChickView(request):
    chick_form = Chick_Model.objects.all()
    return render(request, 'products/chick.html', {'chick_form': chick_form})



# def MedicineView(request):
#     if request.method == "POST":
#         medicine_form = Medicine_Form(request.POST)
#         if medicine_form.is_valid():
#             medicine_form.save()
#             messages.success(request, 'Medicines Added !')
#             medicine_form = Medicine_Form()

#     else :
#         medicine_form = Medicine_Form()
#     return render(request, 'products/medicine.html', {'medicine_form': medicine_form})



def DiseaseView(request):
    if request.method == "POST":
        disease = Disease_Form(request.POST)
        if disease.is_valid():
            disease.save()
            disease = Disease_Form()
            messages.success(request, 'Data Collected !')
            
    else :
        disease = Disease_Form()

    return render(request, "products/disease.html", {'disease': disease})



# def FeedView(request):
#     if request.method == "POST":
#         feed_form = Feed_Form(request.POST)
#         if feed_form.is_valid():
#             feed_form.save()
#             messages.success(request, 'Feed dispached !')
#             feed_form = Medicine_Form()


#     else :
#         feed_form = Medicine_Form()
#     return render(request, 'products/feed.html', {'feed_form': feed_form})



 