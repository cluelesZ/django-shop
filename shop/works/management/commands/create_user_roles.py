from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clients.models import Product
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Создание групп и разрешений'

    def handle(self, *args, **kwargs):
        # Создание групп
        director_group, created = Group.objects.get_or_create(name='Director')
        seller_group, created = Group.objects.get_or_create(name='Seller')
        hr_group, created = Group.objects.get_or_create(name='HR')

        # Получение разрешений для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        product_permissions = {
            'add_product': 'Can add product',
            'change_product': 'Can change product',
            'delete_product': 'Can delete product',
            'view_product': 'Can view product',
        }

        for codename, name in product_permissions.items():
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=product_content_type
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создано разрешение: {name}'))

        # Получение разрешений для модели User
        User = get_user_model()
        user_content_type = ContentType.objects.get_for_model(User)

        user_permissions = {
            'add_user': 'Can add user',
            'change_user': 'Can change user',
            'delete_user': 'Can delete user',

        }

        for codename, name in user_permissions.items():
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=user_content_type
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создано разрешение: {name}'))

        # Назначение разрешений группам
        director_group.permissions.set(Permission.objects.filter(codename__in=product_permissions.keys()))
        seller_group.permissions.set(Permission.objects.filter(codename__in=['change_product']))
        hr_group.permissions.set(Permission.objects.filter(codename__in=user_permissions.keys()))

        self.stdout.write(self.style.SUCCESS('Группы и разрешения созданы успешно'))
