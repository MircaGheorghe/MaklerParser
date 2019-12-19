import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from time import sleep as sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class getMakler:
    def __init__(self, base_url, headers):
        try:
            session = requests.Session()
            request = session.get(base_url, headers = headers)
            if request.status_code == 200:
                self.soup = bs(request.content, 'html.parser')
        except:
            print("Eroare")
        self.get_specification()


    def get_general_information(self): #Get title, price, currency, content, city, phone
        div_header = self.soup.find_all('div', attrs={'class': 'title clrfix'})
        post_title = div_header[0].find('strong', attrs={'id': 'anNameData'}).text
        phone = self.soup.find("ul", attrs={'class', 'hlist clrfix'}).text.strip()
        self.city = self.soup.find('div', attrs={'class', 'item_title_info'}).find_all('span')[0].text
        return post_title, self.city, phone

    def get_post_price_currency(self):
        div_header = self.soup.find_all('div', attrs={'class': 'title clrfix'})
        try:
            post_price = div_header[0].find('div', attrs={'class': 'item_title_price'}).text
            currency = post_price[-1:]
            post_price = post_price[:-1].strip()
            post_price = post_price.replace(' ', '')
            return post_price, currency
        except:
            post_price = None
            currency = None
            return post_price, currency

    def get_region(self):
        city_transnistria = ['Tiraspol', 'Bender', 'Râbnița', 'Blijinii Hutor', 'Grigoriopol', 'Dnestrovsc','Dubăsari', 'Camenca', 'Maiac', 'Tiraspolul Nou', 'Parcani', 'Dnestrovsc','Первомайск', 'Slobozia','Sucleia','Ternovca']
        region = "Moldova"
        if self.city in city_transnistria:
            region = "Transnistria"
        return region
    def get_content(self):
        content = self.soup.find('div', attrs={'class', 'ittext'}).text.strip()
        content = content.replace('[email protected]', '')
        return content

    def get_categories(self):
        categories = self.soup.find_all('li', attrs={'class': 'pl'})
        list_cat = []
        for category in categories[1:]:
            list_cat.append(category.find('a').text.strip())
        return list_cat


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
                img_count = i
            return img_count
        except:
            return False

    def get_specification(self):
        try:
            uls = self.soup.find_all('ul', attrs={'class': 'itemtable box-columns'})
            self.specifications = {}
            for ul in uls:
                for li in ul.find_all('li'):
                    title = li.find("div", attrs={"class": "fields"}).text.strip()
                    value = li.find("div", attrs={"class": "values"}).text.strip()
                    self.specifications[title] = value
            return self.specifications
        except:
            return False


    def get_district(self):
        sectorul = self.specifications['Sectorul']
        return sectorul

    def get_ipoteca(self):
        uls = self.soup.find_all('ul', attrs={'class': 'itemtable'})
        data = {}
        for ul in uls:
            for li in ul.find_all('li'):
                title = li.find("div", attrs={"class": "fields"}).text.strip()
                value = li.find("div", attrs={"class": "values"}).text.strip()
                data[title] = value

        try:
            if data['Ipoteca'] =='✔':
                return True
        except:
            return False


class pasteMakler:
    def __init__(self, user_name, password):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver", options=chrome_options)
        self.driver.get("https://makler.md/md/")
        self.driver.implicitly_wait(3)
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
        self.driver.find_element_by_xpath("//select[@id='region']/option[text()='"+ region +"']").click()
        self.driver.find_element_by_xpath("//select[@id='city']/option[text()='"+ city +"']").click()
        self.driver.find_element_by_xpath("//select[@id='district']/option[text()='"+ district +"']").click()

    def check_ipoteca(self, atribute):
        if atribute == True:
            self.driver.find_element_by_class_name('newAdForm_checkboxField').click()
            self.driver.find_element_by_id('approve-conditions').click()
        else:
            pass

    def complete_title_content(self, post_title, content):
        self.driver.find_element_by_id("editorName").send_keys(post_title)
        self.driver.find_element_by_id("editorText").send_keys(content)


    def complete_price(self, post_price, currency):
        if post_price != None and currency != None:
            element = self.driver.find_element_by_id("price")
            element.send_keys(post_price)

            curency_tab = {
                '$':'USD',
                '₴':'UAH',
                '€':'EUR',
                'lei':'MDL'
            }
            sleep(1)
            if currency in curency_tab.keys():
                get_currency_div = self.driver.find_element_by_class_name('newAdForm_radioBoxButtons')
                elements = get_currency_div.find_elements_by_tag_name('label')
                for element in elements:
                    if element.text == curency_tab[currency]:
                        element.click()
        else:
            pass


    def upload_images(self, nr_img):
        if nr_img != False:
            sleep(1)
            element = self.driver.find_element_by_class_name("qq-upload-button")

            for i in range(nr_img):
                elm = self.driver.find_element_by_xpath("//input[@type='file']")
                elm.send_keys("C://Users/Gheorghe/OneDrive/Documents/Python/work/img/"+ str(i) +".jpg")
        else:
            pass


    def complete_specification(self, specifications):
        if specifications != False:
            element = self.driver.find_element_by_class_name('zend_form')
            #variabila ce contine elementele de pe pagina de incarcare a datelor
            labels = element.find_elements_by_class_name('newAdForm_boxFieldLabel')
            #variabila cu datele de pe pagina de luare a datelor
            keys = specifications.keys()

            #fell of the category inputs
            for label in labels:
                for key in keys:
                    if key in label.text or key == label.text:
                        li = label.find_element_by_xpath('..')
                        select_ = li.find_elements_by_tag_name('select')
                        optgroup = li.find_elements_by_tag_name('optgroup')
                        if select_:
                            try:
                                li.find_element_by_xpath("//select/optgroup/option[text()='" + specifications[key] +"']").click()
                            except:
                                li.find_element_by_xpath("//select/option[text()='" + specifications[key] +"']").click()
                            break

                        if li.find_elements_by_css_selector("input[type='text']"):
                            data = specifications[key].replace('cm', '')
                            data = data.replace('ari', '')
                            data = data.replace('m²', '').strip()
                            li.find_element_by_css_selector("input[type='text']").send_keys(data)
                            break
                        if li.find_elements_by_css_selector("input[type='checkbox']"):
                            additional = ['Încălzire', 'Electricitate', 'Apă', 'Telefon, TV, internet', 'Suplimentar', 'Lângă casă']
                            for add in additional:
                                if add in specifications.keys():
                                    data = specifications[add]
                                    data = data.split(',')
                                    for elem in data:
                                        li.find_element_by_xpath('//label[contains(text(), "' + elem.strip() + '")]').click()

        else:
            pass


    def paste_post(self):
        self.driver.find_element_by_id('phone-37368035704').click()
        self.driver.find_element_by_class_name('saveBtn').click()

    def quit_driver(self):
        self.driver.quit()

