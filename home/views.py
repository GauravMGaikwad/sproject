from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .forms import LoginForm
import requests
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm
import requests

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user but don't commit yet
            user = form.save(commit=False)
            # Ensure password is hashed correctly
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the database
            
            # Log the user in automatically
            login(request, user)
            print(f"User registered: {user.username}, Password: {user.password}")
            # Redirect to the dashboard
            return redirect('dashboard')
    else:
        form = RegisterForm()

        print(f"Register form errors: {form.errors}")
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # If form is valid, attempt to authenticate
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Log and display form errors
            print(f"Login form errors: {form.errors.as_data()}")  # Detailed errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def dashboard(request):
    # Get the API response
    response = requests.get("https://5sim.net/v1/guest/countries")
    countries = response.json()

    # Extract country names
    country_names = [country_data['text_en'] for country_data in countries.values()]
    return render(request, 'dashboard.html', {
        'country_names': country_names,  # Pass the country names to the template
        'username': request.user.username
    })

def numrent(request):
    response = requests.get("https://5sim.net/v1/guest/countries")
    countries = response.json()

    # Extract country names
    country_names = [country_data['text_en'] for country_data in countries.values()]

    return render(request, 'numrent.html', {
        'country_names': country_names,  # Pass the country names to the template
        'username': request.user.username
    })


def get_products(request):
    country = request.GET.get('country', 'any')  # Get country from query parameter
    print(f"Fetching products for country: {country}")  # Debug log
    
    operator = 'any'  # Set the operator
    url = f'https://5sim.net/v1/guest/products/{country}/{operator}'

    try:
        # Fetch basic product information from the first API
        response = requests.get(url, headers={'Accept': 'application/json'}, timeout=10)
        response.raise_for_status()  # Handle HTTP errors
        data = response.json()  # Parse API response
        return JsonResponse(data)  # Send JSON response with basic product data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")  # Debug log
        return JsonResponse({'error': 'Failed to fetch product data'}, status=500)


def get_product_details(request):
    country = request.GET.get('country', 'any')  # Get country from query parameter
    operator = 'any'  # Set the operator
    product = request.GET.get('product', '')  # Get product from query parameter

    # API Token for authorization
    token = ''
    try:
        # Fetch detailed product information from the second API
        additional_url = f'https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}'
        headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
        response = requests.get(additional_url, headers=headers, timeout=10)
        response.raise_for_status()  # Handle HTTP errors
        data = response.json()  # Parse API response
        print(f"API response data: {data}")  # Debug log

        return JsonResponse(data)  # Send JSON response with detailed product data
    
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product details: {e}")  # Debug log
        return JsonResponse({'error': 'Failed to fetch product details'}, status=500)
    

def logout_view(request):
    logout(request)
    return redirect('login') 