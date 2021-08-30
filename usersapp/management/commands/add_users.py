from random import choice, randint
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


FIRST_NAMES = ['Soila', 'Jamison', 'Cleta', 'Phuong', 'Rod', 'Chin', 'Margit', 'Elton', 'Bula', 'Anibal', 'Danyell', 'Carly', 'Janetta', 'Willette', 'Deena', 'Garnet', 'Harris', 'Cori', 'Chi', 'Hank', 'Jerrell', 'Renata', 'Nidia', 'Blossom', 'Nicky', 'Chassidy', 'Gisele', 'Lavinia', 'Amberly', 'Beckie', 'Waylon', 'Enola', 'Sid', 'Gerda', 'Janyce', 'Beverly', 'Tim', 'Harold', 'Edyth', 'Thuy', 'Olen', 'Joane', 'Elsie', 'Kacey', 'Eric', 'Thersa', 'Sheilah', 'Trenton', 'Mimi', 'Halina']
LAST_NAMES = ['Caulfield', 'Ellen', 'Feemster', 'Jumper', 'Mcgrath', 'Grego', 'Bolling', 'Meriwether', 'Damron', 'Colon', 'Tenenbaum', 'Yau', 'Digregorio', 'Schwartz', 'Blizzard', 'Poindexter', 'Hogge', 'Bonham', 'Goodrow', 'Isenhour', 'Boster', 'Tebbs', 'Olivo', 'Feldstein', 'Krider', 'Cavaliere', 'Vanbeek', 'Beiler', 'Gobert', 'Levitt', 'Edler', 'Shryock', 'Brewton', 'Kerney', 'Descoteaux', 'Elkin', 'Stickley', 'Kier', 'Henrichs', 'Duerr', 'Siller', 'Audet', 'Axelson', 'Kester', 'Tallman', 'Stever', 'Gulbranson', 'Fennelly', 'Orwig', 'Ogara']
DOMAINS = ('google.com', 'gmail.com', 'hotmail.com', 'google.cn', 'hotmail.co.jp', 'mail.com.tw', 'replica.org', 'butan.gov', 'smtp.org')


def user_generator():
    while True:
        first = choice(FIRST_NAMES)
        last = choice(LAST_NAMES)
        yield {
            'username': f'{first.lower()}_{last.lower()}_{randint(11, 99)}',
            'first_name': first,
            'last_name': last,
            'email': f'{first[0].lower()}_{last.lower()}{randint(33, 444)}@{choice(DOMAINS)}',
        }


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            default=5,
            help='Number of users to add',
        )
        parser.add_argument(
            '--super',
            action='store_true',
            help='Create standart GeekBrains superuser',
        )

    def handle(self, *args, **options):
        UserModel = get_user_model()
        if options['super']:
            UserModel.objects.filter(is_superuser=True).delete()
            UserModel.objects.create_superuser(
                username='django',
                email='admin@local.host',
                password='geekbrains',
            )
        if options['count']:
            user_data = user_generator()
            for _ in range(options['count']):
                UserModel.objects.create_user(**next(user_data), password='geekbrains')
