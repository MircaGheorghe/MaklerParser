from django.core.management.base import BaseCommand
from robot.parser.include import class_test as test
from robot.models import *
from robot.parser.utils import functions as func
import requests
import time
from datetime import datetime
from time import sleep as sleep
import urllib.request

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
        headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
        try:
            f = open("/home/makler-publication/demofile2.txt", "w")
        except:
            f = open("demofile2.txt", "w")
        while(True):
            try:
                start = time.time()
                for cat in Category.objects.all():
                    is_work = mustPosted.objects.last()
                    if is_work.content:
                        links = func.get_valid_links(cat)
                        print("Au fost verificate link-urile")
                        print(links)
                        if not links:
                            print("Nu sunt link-uri care au trecut validarea")
                            continue
                        l = links[0].account
                        # f.write(str(links[0].content) + str(datetime.now()) + '\n' + str(cat.content))
                        if func.get_last_phone(cat.content):
                            continue
                        print("Link-ul a trecut validarea, poate fi postat")
                        pasteMakler = test.pasteMakler(l.username, l.password)
                        print("S-a logat")
                        getMakler = test.getMakler(links[0].content, headers)
                        print("A luat informaatia")
                        pasteMakler.change_location('https://makler.md/md/an/web/add')
                        print("S-a schimbat pe sectiunea postari")
                        pasteMakler.choose_category(getMakler.get_categories())
                        print("A ales categoria")
                        pasteMakler.complete_adress(getMakler.get_general_information()[1], getMakler.get_district(), getMakler.get_region())
                        print("A ales regiunea")
                        pasteMakler.set_period(getMakler.get_period())
                        print("A setat perioada")
                        pasteMakler.complete_title_content(getMakler.get_general_information()[0], getMakler.get_content())
                        print("A inserat titlul si contentul")
                        pasteMakler.set_proposal(getMakler.get_type_proposal())
                        print("A setat tipul propunerii")
                        pasteMakler.complete_price(getMakler.get_post_price_currency()[0], getMakler.get_post_price_currency()[1])
                        print(getMakler.get_post_price_currency()[1])
                        print("A postat pretul si valuta")
                        # pasteMakler.check_ipoteca(getMakler.get_ipoteca())
                        print("A verificat de ipoteca")
                        pasteMakler.upload_images(getMakler.get_images())
                        print("A postat imaginile")
                        print(getMakler.specifications)
                        pasteMakler.complete_specification(getMakler.specifications)
                        print("A completat specificatiile")

                        rez = False
                        while rez == False:
                            rez = pasteMakler.get_last_load_image()
                        l.author.last_name
                        phone = "phone-" + l.username
                        pasteMakler.paste_post(phone)
                        print("A postat")
                        Link.objects.filter(content=links[0].content).update(posted=True)
                        Link.objects.filter(content=links[0].content).update(post_date=datetime.now())
                        pasteMakler.quit_driver()

                        try:
                            func.send_message(l.author.last_name, links[0].content, l.username, datetime.now())
                        except:
                            pass
                        end = time.time()
                        result = end - start
                        print(result)
                        f.close()
                    print("a fost oprit")
                sleep(3)
            except Exception as e:
                raise e
                # func.send_error_message("A aparut o eroare la postare")