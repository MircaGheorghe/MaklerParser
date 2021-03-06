import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from time import sleep as sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from robot.parser.utils import functions as func
import re
from datetime import datetime
import os
from robot.models import *


class getMakler:
    def __init__(self, base_url, headers):
        try:
            session = requests.Session()
            request = session.get(base_url, headers = headers)
            if request.status_code == 200:
                self.soup = bs(request.content, 'html.parser')
        except:
            pass
        self.get_specification()


    def get_general_information(self): #Get title, price, currency, content, city, phone
        try:
            div_header = self.soup.find_all('div', attrs={'class': 'title clrfix'})
            post_title = div_header[0].find('strong', attrs={'id': 'anNameData'}).text
            phone = self.soup.find("ul", attrs={'class', 'hlist clrfix'}).text.strip()
            self.city = self.soup.find('div', attrs={'class', 'item_title_info'}).find_all('span')[0].text
            return post_title, self.city, phone
        except:
            pass

    def get_post_price_currency(self):
        try:
            div_header = self.soup.find_all('div', attrs={'class': 'title clrfix'})
            post_price = div_header[0].find('div', attrs={'class': 'item_title_price'}).text
            total_currency = ['$', '₴','€', 'Lei']
            for val in total_currency:
                if val in post_price:
                    currency = val
            post_price = post_price[:-1].strip()
            post_price = post_price.replace(' ', '').lower()
            post_price = re.sub(r'[a-zа-я]+', '', post_price, re.I)
            return post_price, currency
        except:
            post_price = None
            currency = None
            return post_price, currency


    def get_region(self):
        try:
            city_transnistria = ['Tiraspol', 'Bender', 'Râbniţa', 'Blijinii Hutor', 'Grigoriopol', 'Dnestrovsc','Dubăsari', 'Camenca', 'Maiac', 'Tiraspolul Nou', 'Parcani', 'Dnestrovsc','Первомайск', 'Slobozia','Sucleia','Ternovca']
            region = "Moldova"
            if self.city in city_transnistria:
                region = "Transnistria"
            return region
        except:
            pass

    def get_content(self):
        try:
            content = self.soup.find('div', attrs={'id': 'anText'}).text
            content = content.replace('[email protected]', '')
            n_c = '\n'.join([row.strip() for row in content.split('\n')])
            removal_list = ['', '\t', '\n']
            for s in removal_list:
                n_c = n_c.replace(s, '')
            return n_c
        except:
            pass

    def get_categories(self):
        try:
            categories = self.soup.find_all('li', attrs={'class': 'pl'})
            list_cat = []
            for category in categories[1:]:
                list_cat.append(category.find('a').text.strip())
            return list_cat
        except:
            pass


    def get_images(self): #Salveaza iamginile in folder si returneaza numarul de imagini
        try:
            div_image = self.soup.find('div', id = "anItemData").find('div', attrs={'class': 'itmedia'})
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)

            i = 0
            for a in div_image.find_all("a"):
                urllib.request.urlretrieve(a['href'], "img/{}.jpg".format(str(i)))
                i += 1
            return i
        except:
            pass


    def get_specification(self):
        try:
            try:
                uls = self.soup.find_all('ul', attrs={'class': 'itemtable'})
            except:
                uls = self.soup.find_all('ul', attrs={'class': 'itemtable box-columns'})
            self.specifications = {}
            for ul in uls:
                for li in ul.find_all('li'):
                    #aici nu gaseste probabil dupa id
                    title = li.find("div", attrs={"class": "fields"}).text.strip()
                    value = li.find("div", attrs={"class": "values"}).text.strip()
                    self.specifications[title] = value
            return self.specifications
        except:
            return False


    def get_district(self):
        try:
            sectorul = self.specifications['Sectorul']
            return sectorul
        except:
            return False

    def get_ipoteca(self):
        try:
            uls = self.soup.find_all('ul', attrs={'class': 'itemtable'})
            data = {}
            for ul in uls:
                for li in ul.find_all('li'):
                    title = li.find("div", attrs={"class": "fields"}).text.strip()
                    value = li.find("div", attrs={"class": "values"}).text.strip()
                    data[title] = value

            if data['Ipoteca'] =='✔':
                    return True
            return False
        except:
            pass

    def get_period(self):
        try:
            perioada = self.soup.find('ul', attrs={'class': 'itemtable'}).find("div", attrs={'class': 'values'}).text.strip()
            return perioada
        except:
            pass

    def get_type_proposal(self):
        try:
            ul = self.soup.find('ul', attrs={'class': 'itemtable'})
            type_prop = ul.find('div', attrs={'class': 'values'}).text.strip()
            return type_prop
        except:
            pass



class pasteMakler:
    def __init__(self, user_name, password):
        chrome_options = Options()
        try:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
        except:
            self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver")

        self.driver.get_screenshot_as_file('screenshots/getBeforePageScreen.png')
        self.driver.get('https://makler.md')
        self.driver.get_screenshot_as_file('screenshots/getAfterPageScreen.png')
        self.driver.implicitly_wait(3)
        self.driver.get_screenshot_as_file('screenshots/sadfsomeError.png')

        try:
            self.driver.find_element_by_class_name('ui-icon-closethick').click()
        except:
            pass
        self.driver.find_element_by_id('logInDiv').click()
        self.driver.find_element_by_name('login').send_keys(user_name, Keys.ARROW_DOWN)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_class_name("popupRedButton").click()


    def change_location(self, location):
        sleep(1)
        self.driver.get(location)


    def choose_category(self, categories):
         for i in range(len(categories)):
            self.driver.find_element_by_xpath("//select[@name='category']/option[text()='"+ categories[i] +"']").click()


    def complete_adress(self, city, district, region):
        sleep(1)
        try:
            self.driver.find_element_by_xpath("//select[@id='region']/option[text()='"+ region +"']").click()
            self.driver.find_element_by_xpath("//select[@id='city']/option[text()='"+ city +"']").click()
            self.driver.find_element_by_xpath("//select[@id='district']/option[text()='"+ district +"']").click()
        except:
            self.driver.get_screenshot_as_file('screenshots/adresa.png')

    def check_ipoteca(self, atribute):
        try:
            self.driver.find_element_by_class_name('newAdForm_checkboxField').click()
            self.driver.find_element_by_id('approve-conditions').click()
        except:
            self.driver.get_screenshot_as_file('screenshots/ipoteca.png')

    def complete_title_content(self, post_title, content):
        try:
            self.driver.find_element_by_id("editorName").send_keys(post_title)
            self.driver.find_element_by_id("editorText").send_keys(content)
        except:
            self.driver.get_screenshot_as_file('screenshots/contentul')


    def complete_price(self, post_price, currency):
        try:
            if post_price != None and currency != None:
                element = self.driver.find_element_by_id("price")
                element.send_keys(post_price)

                curency_tab = {
                    '$':'USD',
                    '₴':'UAH',
                    '€':'EUR',
                    'Lei':'MDL'
                }
                sleep(1)
                if currency in curency_tab.keys():
                    get_currency_div = self.driver.find_element_by_class_name('newAdForm_radioBoxButtons')
                    get_currency_div.find_element_by_xpath('//label[contains(text(), "' + curency_tab[currency] + '")]').click()
        except:
            self.driver.get_screenshot_as_file('screenshots/valuta.png')


    def upload_images(self, nr_img):
        try:
            if nr_img != False:
                sleep(1)
                element = self.driver.find_element_by_class_name("qq-upload-button")

                for i in range(nr_img):
                    elm = self.driver.find_element_by_xpath("//input[@type='file']")
                    dirname = os.path.dirname(__file__)
                    dirname = os.path.abspath(os.path.join(dirname, '../../../'))
                    elm.send_keys("{}/img/{}.jpg".format(dirname, i))
            else:
                self.driver.get_screenshot_as_file('screenshots/imaginile.png')
        except:
            pass


    def complete_specification(self, specifications):
        if specifications != False:
            element = self.driver.find_element_by_class_name('zend_form')
            #variabila ce contine elementele de pe pagina de incarcare a datelor
            labels = element.find_elements_by_class_name('newAdForm_boxFieldLabel')
            #variabila cu datele de pe pagina de luare a datelor
            keys = specifications.keys()

            #fell of the category inputs
            exist = []
            for label in labels:
                for key in keys:
                    if key in label.text or key == label.text:
                        li = label.find_element_by_xpath('..')
                        select_ = li.find_elements_by_tag_name('select')
                        optgroup = li.find_elements_by_tag_name('optgroup')

                        #selectbox
                        if select_:
                            try:
                                li.find_element_by_xpath("//select/optgroup/option[text()='" + specifications[key] +"']").click()
                            except:
                                li.find_element_by_xpath("//select/option[text()='" + specifications[key] +"']").click()
                            break

                        #inputbox
                        if li.find_elements_by_css_selector("input[type='text']"):
                            data = specifications[key].replace('cm', '')
                            data = data.replace('ari', '')
                            data = data.replace('m²', '').strip()
                            li.find_element_by_css_selector("input[type='text']").send_keys(data)
                            break

                        #checkbox
                        additional = ['Încălzire', 'Electricitate', 'Apă', 'Telefon, TV, internet', 'Suplimentar', 'Lângă casă', 'Tipul de imobiliare', 'Comunicaţii', 'Intrare']
                        for add in additional:
                            if add not in exist:
                                if add in specifications.keys():
                                    data = specifications[add]
                                    data = data.split(',')
                                    exist.append(add)
                                    for elem in data:
                                        elem = elem.strip()
                                        li.find_element_by_xpath('//label[contains(text(), "' + elem + '")]').click()
                        for spec in specifications.keys():
                            spec = spec.strip()
                            if specifications[spec] == '✔':
                                li.find_element_by_xpath('//label[contains(text(), "' + spec + '")]').click()

        else:
            self.driver.get_screenshot_as_file('screenshots/specificatiile.png')

    def set_period(self, period):
        try:
            if period != None and period != '':
                element = self.driver.find_element_by_class_name('newAdForm_fieldBox')
                element.find_element_by_xpath("//select[@name='field_432']/option[text()='"+ period +"']").click()
        except:
            self.driver.get_screenshot_as_file('screenshots/perioada.png')

    def set_proposal(self, proposal):
        arr = []
        try:
            arr = proposal.split(', ')
        except:
            arr.append(proposal)
        try:
            if len(arr) > 1:
                div = self.driver.find_element_by_id('kind')
                if arr[0] == "vând":
                    div.find_elements_by_tag_name('label')[0].click()
                    div = self.driver.find_element_by_id('newAdForm_isForChangeBox')
                    div.find_element_by_tag_name('label').click()
                    return
                div.find_elements_by_tag_name('label')[1].click()
                div = self.driver.find_element_by_id('newAdForm_isForChangeBox')
                div.find_element_by_tag_name('label').click()
                return
            div = self.driver.find_element_by_id('kind')
            if proposal == "vând":
                div.find_elements_by_tag_name('label')[0].click()
                return
            div.find_elements_by_tag_name('label')[1].click()
        except:
            pass

    def get_last_load_image(self):
        try:
            element = self.driver.find_element_by_id('files_list')
            img = element.find_elements_by_tag_name('li')[0].find_element_by_tag_name('label').find_element_by_tag_name("span").get_attribute("style")
            if img == "display: none;":
                return True
            return False
        except:
            pass


    def paste_post(self, phone):
        sleep(2)
        self.driver.find_element_by_id(phone).click()
        self.driver.find_element_by_class_name('saveBtn').click()
        try:
            self.driver.find_element_by_id('confirm_dialog').find_element_by_class_name('buttons').find_element_by_tag_name(a).click()
        except:
            self.driver.get_screenshot_as_file('screenshots/postare.png')

    def get_new_link(self):
        sleep(2)
        self.driver.get('https://makler.md/md/an/my/')
        div = self.driver.find_element_by_class_name('descr')
        div.find_element_by_class_name('title').click()
        return self.driver.current_url

    def quit_driver(self):
        self.driver.quit()

