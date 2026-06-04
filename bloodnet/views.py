from django.shortcuts import render,redirect
from .models import *
from .form import *

# Create your views here.

def donor_add(request):

    
    if request.method=='POST':
        donor_data=donor_form(request.POST)
        
        if donor_data.is_valid():   
            donor_data.save()
            return redirect('/donor/view/')

            

    context={
        'donor_form':donor_data
    }
    
    return render(request,'donor_form.html',context)

def  Donor_view(request):

    context={
        'all_donor':add_donors.objects.all()

    }
    return render(request,'add_donor.html',context)

def donor_delete(request,id):
    deleted_donor=add_donors.objects.get(id=id)
    deleted_donor.delete()
    return redirect('/donor/view/')
def donor_update(request,id):
    updated_donor=add_donors.objects.get(id=id)

    context={
        'donor_forms':donor_form(instance=updated_donor)
    }   

    if request.method == 'POST':
        updated=donor_form(request.POST,instance=updated_donor)
        if updated.is_valid():
            updated.save()
            return redirect('/donor/view/')
        
    return render(request,'donor_form.html',context)