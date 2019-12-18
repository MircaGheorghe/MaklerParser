from datetime import datetime
from robot.models import *
from datetime import timedelta

def get_valid_links(cat):
    date_24h = datetime.now() - timedelta(hours=24)
    links = Link.objects.filter(category=cat, post_date__lt = date_24h)
    if links:
        return links
    return Link.objects.filter(category=cat, payment = True)