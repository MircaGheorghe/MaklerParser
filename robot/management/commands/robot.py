from django.core.management.base import BaseCommand
from robot.parser.include import class_test as test
from robot.models import *
from robot.parser.utils import functions as func
import requests
import time




class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

        start = time.time()
        print("ceva")
        for cat in Category.objects.all():
            print("categoria")
            links = func.get_valid_links(cat)
            print("am verificat link-ul")
            if not links:
                print("son")
                continue
            l = links[0].account
            if not func.get_last_phone(cat.content):
                continue
            print("a trecut verificarea, poate fi postat")
            pasteMakler = test.pasteMakler(l.username, l.password)
            print("S-a logat")
            getMakler = test.getMakler(links[0].content, headers)
            print("a luat informaatia")
            pasteMakler.change_location('https://makler.md/md/an/web/add')
            print("Sa schimbat pe sectiunea postari")
            pasteMakler.choose_category(getMakler.get_categories())
            print("A ales categoria")
            pasteMakler.complete_adress(getMakler.get_general_information()[1], getMakler.get_district(), getMakler.get_region())
            print("a ales regiunea")
            pasteMakler.complete_title_content(getMakler.get_general_information()[0], getMakler.get_content())
            print("a inserat titlul si contentul")
            pasteMakler.complete_price(getMakler.get_post_price_currency()[0], getMakler.get_post_price_currency()[1])
            print("a postat pretul si valuta")
            pasteMakler.check_ipoteca(getMakler.get_ipoteca())
            print("a verificat de ipoteca")
            pasteMakler.upload_images(getMakler.get_images())
            print("a postat imaginile")
            pasteMakler.complete_specification(getMakler.specifications)
            print("a completat specificatiile")
            phone = "phone-" + l.username
            pasteMakler.paste_post(phone)
            print("a postat")
            pasteMakler.quit_driver()

            end = time.time()
            result = end - start
            print(result)
