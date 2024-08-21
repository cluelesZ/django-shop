from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    # Создаем группы, если они не существуют
    for role in ['Director', 'Seller', 'HR']:
        group, created = Group.objects.get_or_create(name=role)

    # Списки разрешений
    director_permissions = ['add_product', 'change_product', 'delete_product', 'add_user', 'change_user', 'delete_user']
    seller_permissions = ['change_product']
    hr_permissions = ['add_user', 'change_user', 'delete_user']

    # Получаем группы
    director_group = Group.objects.get(name='Director')
    seller_group = Group.objects.get(name='Seller')
    hr_group = Group.objects.get(name='HR')

    # Добавляем разрешения для директора
    for perm in director_permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            director_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission with codename '{perm}' does not exist.")

    # Добавляем разрешения для продавца
    for perm in seller_permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            seller_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission with codename '{perm}' does not exist.")

    # Добавляем разрешения для HR
    for perm in hr_permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            hr_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission with codename '{perm}' does not exist.")
