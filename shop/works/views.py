from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from clients.models import Product
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User

# Добавление продукта
@permission_required('clients.add_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'works/add_product.html', {'form': form})

# Редактирование продукта
@permission_required('clients.change_product')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'works/edit_product.html', {'form': form, 'product': product})

# Удаление продукта
@permission_required('clients.delete_product')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'works/delete_product.html', {'product': product})

# Список продуктов
def product_list(request):
    products = Product.objects.all()
    return render(request, 'works/product_list.html', {'products': products})

# Добавление пользователя (HR)
@permission_required('auth.add_user')
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            group = Group.objects.get(name=role)
            user.groups.add(group)
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'works/add_user.html', {'form': form})

# Список пользователей
@permission_required('auth.view_user')
def user_list(request):
    users = User.objects.all()
    return render(request, 'works/user_list.html', {'users': users})

# Дашборд
@login_required
def dashboard(request):
    context = {
        'user': request.user,  # Передаем пользователя в контекст
    }
    return render(request, 'works/dashboard.html', context)

def main(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # перенаправление на главную страницу после входа
    else:
        form = AuthenticationForm()
    return render(request, 'works/login.html', {'form': form})