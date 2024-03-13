from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.template import loader
import json
from django.urls import reverse





def index(request):
    return render(request, 'store/index.html')


# Vues pour les pages principales

def about(request):
    return render(request, "store/about.html")

def contact(request):
    return render(request, "store/contact.html")

def voiture(request):
    return render(request, "store/voiture.html")

def chambre(request):
    return render(request, "store/chambre.html")

def restaurant(request):
    return render(request, "store/restaurant.html")

# def detailvoiture(request):
#     return render(request, "store/detailvoiture.html")


# Vues pour l'authentification
def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        hashed_password = make_password(password)
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO utilisateur (id,nom, email, PASSWORD) VALUES (null, %s, %s, %s)", [full_name, email, hashed_password])
                connection.commit()
            return redirect('index')
        except Exception as e:
            print(str(e))
            messages.error(request, 'Error occurred during signup.')
    
    return render(request, "site_reservation/login.html")



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM utilisateur WHERE email = %s", [email])
            user = cursor.fetchone()

            if user is not None and check_password(password, user[3]):
                print(user[3])
                print('\n')
                print('*****************************')
                print(password)
                request.session['user'] = { 'id' : user[0], 'nom' : user[1], 'email': user[2]}
                redirect_to = request.POST.get('next') or reverse('index')
                return redirect(redirect_to)
            else:
                messages.error(request, 'Invalid credentials')
    
    return render(request, "site_reservation/login.html")

def logout_view(request):
    del request.session['user']
    return redirect('index')


