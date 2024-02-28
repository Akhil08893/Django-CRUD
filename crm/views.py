from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,AddRecord
from .models import Record

def home(request):
    record=Record.objects.all()
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request,"please enter the correct credentials")
            return redirect('home')
    else:
        return render(request,'home.html',{'record':record})

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method =='POST':
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer':customer})
    else:
        messages.success(request,"You must be login...")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete = Record.objects.get(id=pk)
        delete.delete()
        messages.success(request,"Record Deleted successful..")
        return redirect('home')
    else:
        messages.success(request,"You must be login...")
        return redirect('home')
    
def add_record(request):
    form=AddRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record Added ")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"You must be Login")
        return redirect('home')

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form = AddRecord(request.POST or None , instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record updated... ")
            return redirect('home')
        return render(request,'update.html',{'form':form})
    else:
        messages.success(request,"You must be Login")
        return redirect('home')