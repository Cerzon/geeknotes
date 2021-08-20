from random import choice, randint


FIRST_NAMES = ['Soila', 'Jamison', 'Cleta', 'Phuong', 'Rod', 'Chin', 'Margit', 'Elton', 'Bula', 'Anibal', 'Danyell', 'Carly', 'Janetta', 'Willette', 'Deena', 'Garnet', 'Harris', 'Cori', 'Chi', 'Hank', 'Jerrell', 'Renata', 'Nidia', 'Blossom', 'Nicky', 'Chassidy', 'Gisele', 'Lavinia', 'Amberly', 'Beckie', 'Waylon', 'Enola', 'Sid', 'Gerda', 'Janyce', 'Beverly', 'Tim', 'Harold', 'Edyth', 'Thuy', 'Olen', 'Joane', 'Elsie', 'Kacey', 'Eric', 'Thersa', 'Sheilah', 'Trenton', 'Mimi', 'Halina']
LAST_NAMES = ['Caulfield', 'Ellen', 'Feemster', 'Jumper', 'Mcgrath', 'Grego', 'Bolling', 'Meriwether', 'Damron', 'Colon', 'Tenenbaum', 'Yau', 'Digregorio', 'Schwartz', 'Blizzard', 'Poindexter', 'Hogge', 'Bonham', 'Goodrow', 'Isenhour', 'Boster', 'Tebbs', 'Olivo', 'Feldstein', 'Krider', 'Cavaliere', 'Vanbeek', 'Beiler', 'Gobert', 'Levitt', 'Edler', 'Shryock', 'Brewton', 'Kerney', 'Descoteaux', 'Elkin', 'Stickley', 'Kier', 'Henrichs', 'Duerr', 'Siller', 'Audet', 'Axelson', 'Kester', 'Tallman', 'Stever', 'Gulbranson', 'Fennelly', 'Orwig', 'Ogara']
DOMAINS = ('google.com', 'gmail.com', 'hotmail.com', 'google.cn', 'hotmail.co.jp', 'mail.com.tw', 'replica.org', 'butan.gov', 'smtp.org')


def geek_user_generator():
    while True:
        first = choice(FIRST_NAMES)
        last = choice(LAST_NAMES)
        yield {
            'username': f'{first.lower()}_{last.lower()}_{randint(11, 99)}',
            'first_name': first,
            'last_name': last,
            'email': f'{first[0].lower()}_{last.lower()}{randint(33, 444)}@{choice(DOMAINS)}',
        }
