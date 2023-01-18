from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages,auth
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    return render(request,'all_emp.html',{'emps':emps})

def add_emp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = request.POST['salary']
        dept = int(request.POST['dept'])
        bonus = request.POST['bonus']
        role = int(request.POST['role'])
        phone = request.POST['phone']
        emp = Employee(first_name=first_name,last_name=last_name,salary=salary,dept_id=dept,bonus=bonus,role_id=role,phone=phone,hire_date=datetime.now())
        emp.save()
        return HttpResponse(" <h1> Employee Added Successfully! </h1>")
    elif request.method == "POST":
        return redirect("all_emp")
    else:
        return render(request,'add_emp.html')


def remove_emp(request,id=0):
    if id:
        try:
            emp_removed = Employee.objects.get(id = id)
            emp_removed.delete()
            return HttpResponse(" <h1> Employee Removed Successfully! </h1>")
        except:
            return HttpResponse("Please Enter A Valid Emp ID")
    emps = Employee.objects.all()
    return render(request,'remove_emp.html',{'emps':emps})


def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']

        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name)  | Q(last_name__icontains = name) )
        if dept:
            emps = emps.filter(Q(dept__name__icontains = dept))
        if role:
            emps = emps.filter(Q(role__name__icontains = role))
        return render(request,'all_emp.html',{'emps':emps})
    elif request.method == "GET":
        return render(request,'filter_emp.html')
    else:
        return HttpResponse("An Error Occured")


#  ----------  Authentication and Autherization ----------------------

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid Username or Passowrd")
            return redirect("/login")
    else:
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")


    