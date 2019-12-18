from django.core.management.base import BaseCommand
from robot.parser.include import class_test as test
from robot.models import *
from robot.parser.utils import functions as func
import requests


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }


        for cat in Category.objects.all():
            links = func.get_valid_links(cat)
            if not links:
                continue
            l = links[0].account
            func.get_last_phone(cat.content)
            # pasteMakler = test.pasteMakler(l.username, l.password)
            getMakler = test.getMakler(links[0].content, headers)
            pasteMakler.change_location('https://makler.md/md/an/web/add')
            pasteMakler.choose_category(getMakler.get_categories())

            pasteMakler.complete_adress(getMakler.get_general_information()[1], getMakler.get_district(), getMakler.get_region())
            pasteMakler.complete_title_content(getMakler.get_general_information()[0], getMakler.get_content())
            pasteMakler.complete_price(getMakler.get_post_price_currency()[0], getMakler.get_post_price_currency()[1])
            pasteMakler.check_ipoteca(getMakler.get_ipoteca())
            pasteMakler.upload_images(getMakler.get_images())
            pasteMakler.complete_specification(getMakler.specifications)
            pasteMakler.paste_post()
            pasteMakler.quit_driver()