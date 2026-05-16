from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import UserForm, SalesmanForm
from accounts.models import Company, CustomerProfile, SalesmanProfile

def salesman_register_view(request):
    title = 'Register Salesman'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_salesman = True  # Default role
            user.save()
            # login(request, user)
            messages.success(request, "Salesman Registration successful.")
            return redirect('reports:admin-dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form, 'title': title})

def update_salesman(request, pk):
    salesman = SalesmanProfile.objects.get(pk=pk)
    if request.method == 'POST':
        form = SalesmanForm(request.POST, instance=salesman)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            if request.user.is_salesman:
              return redirect('reports:salesman-dashboard')
            if request.user.is_admin:
              return redirect('reports:admin-dashboard')
        else:
            messages.error(request, "Unsuccessful update. Invalid information.")
    else:
        form = SalesmanForm(instance=salesman)
    return render(request, 'profile_form.html', {'form': form, 'title': 'Update Salesman'})

def customer_register_view(request):
    title = 'Register Customer'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True  # Default role
            user.save()
            # login(request, user)
            messages.success(request, "Customer Registration successful.")
            return redirect('reports:admin-dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form, 'title': title})

def login_view(request):
    company = Company.objects.first()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            if request.user.is_admin:
              return redirect('reports:admin-dashboard')
            
            if request.user.is_salesman:
              return redirect('reports:salesman-dashboard')
            
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'company': company})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')

def salesman_list(request):
    salesman_list = SalesmanProfile.objects.all()
    return render(request, 'salesman_list.html', {'salesmen': salesman_list})

def customers_list(request):
    customers_list = CustomerProfile.objects.all()
    return render(request, 'customers_list.html', {'customers': customers_list})