from django.shortcuts import render
from base import models
from base.models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def skills(request):
    return render(request, 'skills.html')

def projects(request):
    return render(request, 'projects.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        content = request.POST.get('content')

        # Validaciones (como ya las tienes)
        if len(name) < 2 or len(name) > 30:
            messages.error(request, 'Length of name should be between 2 and 30 characters.')
            return render(request, 'home.html')
        if len(email) < 5 or len(email) > 40:
            messages.error(request, 'Invalid email, please try again.')
            return render(request, 'home.html')
        if len(number) < 10 or len(number) > 12:
            messages.error(request, 'Invalid number, please try again.')
            return render(request, 'home.html')

        # Guardar en la base de datos
        ins = models.Contact(name=name, email=email, content=content, number=number)
        ins.save()

        # Enviar correo
        subject = f'Nuevo mensaje de contacto de {name}'
        message = f'''
        Has recibido un nuevo mensaje desde tu portfolio:

        Nombre: {name}
        Email: {email}
        Número: {number}
        Mensaje:
        {content}
        '''
        from_email = settings.EMAIL_HOST_USER
        to_email = ['brayanvilla844@gmail.com']  # Puedes cambiar este por el tuyo
        send_mail(subject, message, from_email, to_email, fail_silently=False)


        messages.success(request, '¡Gracias por contactarme! Te responderé pronto.')
    return render(request, 'contact.html')

def game_menu(request):
    return render(request, 'game_menu.html')
