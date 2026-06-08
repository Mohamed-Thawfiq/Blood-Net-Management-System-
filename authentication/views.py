from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout
from .models import *
# Create your views here.
# def loginpage(request):

#     if request.method=='POST':
#         print(request.POST)
    

#     return render(request,'login.html')

class loginpage(View):

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/donor/view/')

        context = {
            'error': 'Invalid username or password.',
            'form_data': {
                'username': username,
            }
        }
        return render(request, 'login.html', context)
    
class logoutuser(View):
    def get(self,request):
        logout(request)
        return redirect('/')

        
    
class registerpage(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        contact = request.POST.get('contact_num', '').strip()
        email = request.POST.get('email_address', '').strip()
        area = request.POST.get('area_name', '').strip()
        id_num = request.POST.get('id_no', '').strip()
        acc_type = request.POST.get('acc_type', '')

        error = None
        if not username or not password or not contact or not email or not area or not id_num or not acc_type:
            error = 'Please fill in all registration fields.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already exists. Choose a different username.'
        elif User.objects.filter(id_num=id_num).exists():
            error = 'Membership Card ID already exists. Use a different ID.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'

        if error:
            context = {
                'error': error,
                'form_data': {
                    'username': username,
                    'contact_num': contact,
                    'email_address': email,
                    'area_name': area,
                    'id_no': id_num,
                    'acc_type': acc_type,
                }
            }
            return render(request,'register.html',context)

        role_value = 1 if acc_type == 'manager' else 2 if acc_type == 'donor' else 0
        new_user = User(
            username=username,
            contact=contact,
            email=email,
            area=area,
            id_num=id_num,
            role=role_value,
        )
        new_user.set_password(password)
        new_user.save()
        return redirect('/')
