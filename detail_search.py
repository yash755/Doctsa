import requests
from bs4 import BeautifulSoup
import csv
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import datetime
import re


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())


file = open('main_file_2.txt','r')

for f in file:
    f = f.replace('\n','')
    f = f.split('===')

    url = f[1]

    print(url)
    driver.get(str(url))


    try:
        driver.execute_script("arguments[0].click();", driver.find_elements_by_xpath("//a[text()='More about This Attorney']")[0])

    except:
        print("Eror")


    html2 = driver.page_source
    html = BeautifulSoup(html2, "lxml", from_encoding="utf-8")

    full_name = f[0]
    full_name = full_name.split(',',1)

    first_name = full_name[0]

    if len(full_name) >=2:
        last_name = full_name[1]
    else:
        last_name = ''
    address = ''
    phone = ''
    fax = ''
    email = ''
    website = ''
    cla_section = ''
    law_school = ''
    languages = ''
    licnese = ''

    paras = html.find_all('p')


    for p in paras:
        p_text = p.text.strip()

        if address == '':
            if 'Address' in p_text:
                address = p_text
                address = address.replace('Address:','')
                address = address.strip()
                print(address)

        if phone == '':
            if 'Phone' in p_text:
                p_text =p_text.replace('\n','')
                p_text = p_text.split('Fax:')

                if len(p_text) >=1:
                    phone = p_text[0]
                    phone = phone.replace('Phone:', '')
                    phone = phone.replace('|','')
                    phone = phone.strip()
                    print(phone)

                if len(p_text) >=2:
                    fax = p_text[1]
                    fax = fax.strip()
                    print(fax)


        if email == '':
            if 'Email' in p_text:

                paras_p = p.find_all('span')

                for para in paras_p:
                    id = para.get('id')

                    try:
                        cssValue = driver.find_element_by_id(id)
                        cssValue = cssValue.value_of_css_property("display")

                        if str(cssValue) == 'inline':
                            email = para.text.strip()
                            print(email)
                            break
                    except:
                        print("Eror")


                p_text = p_text.replace('\n', '')
                p_text = p_text.split('Website:')

                if len(p_text) >=2:
                    website = p_text[1]
                    website = website.strip()
                    print(website)

        if law_school == '':
            if 'Law School' in p_text:
                law_school = p_text
                law_school = law_school.replace('Law School:','')
                law_school = law_school.strip()
                print(law_school)

        if languages == '':
            if 'Additional Languages Spoken' in p_text:
                try:
                    ul_para = p.find_next_sibling('ul')
                    lis = ul_para.find_all('li')
                    for li in lis:
                        li_text = li.text.strip()
                        li_text = li_text.replace('\n','')
                        li_text = li_text.split(':')

                        if len(li_text) == 2:
                            li_text_string = li_text[0].strip() + ':' + li_text[1].strip()
                            languages = languages + li_text_string + ','

                except:
                    print("eror")



    rows = html.find_all('div',{'class':'row'})

    for row in rows:
        row_text = row.text.strip()

        if 'CLA Sections' in row_text:
            cla_section = row_text
            cla_section = cla_section.replace('\n','')
            cla_section = cla_section.replace('CLA Sections','')
            cla_section = cla_section.replace(':', '')
            print(cla_section)

    divs = html.find_all('b')

    for div in divs:
        div_text = div.text.strip()

        if licnese == '':
            if 'License Status' in div_text:
                licnese = div_text
                licnese = licnese.replace('License Status','')
                licnese = licnese.replace(':', '')
                licnese = licnese.strip()
                print(licnese)
                break

    temp = []
    temp.append(url)
    temp.append(first_name)
    temp.append(last_name)
    temp.append(address)
    temp.append(phone)
    temp.append(fax)
    temp.append(email)
    temp.append(website)
    temp.append(cla_section)
    temp.append(law_school)
    temp.append(languages)
    temp.append(licnese)

    arr = []
    arr.append(temp)

    with open('main_data.csv', 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerows(arr)





driver.close()