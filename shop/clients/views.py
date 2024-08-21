from django.shortcuts import render
from .models import Product
from django.contrib.auth.models import User

def clients_main(request):
    products = Product.objects.all()  # Получаем все продукты из базы данных
    users = User.objects.all()  # Получаем всех пользователей из базы данных
    context = {
        'products': products,
        'users': users,
    }
    return render(request, 'clients/main.html', context)
