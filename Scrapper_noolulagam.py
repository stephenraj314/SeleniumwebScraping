from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import platform
import csv

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--log-level=3")
sys_Platform = platform.system()
if sys_Platform == 'Windows' :
    DRIVER_PATH = 'chromedriver_win32\chromedriver.exe'
elif sys_Platform == 'Linux' :
    DRIVER_PATH = '/chromedriver_linux64/chromedriver'
elif sys_Platform == 'Darwin' :
    DRIVER_PATH = '/chromedriver_mac64/chromedriver'

i=0
all_details=[]
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("http://www.noolulagam.com/books")


# scrap book details from மேலும் படிக்க... link
while i<10:
    link = "//div[@id='content']/table/tbody/tr[{0}]/td/table/tbody/tr[2]/td/a"
    link2 = "//div[@id='content']/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[{0}]/td[3]"
    driver.find_element_by_xpath(link.format(i+2)).click()
    driver.get(driver.current_url)
    title = driver.find_element_by_xpath("//div[@id='content']/table/tbody/tr/td/table/tbody/tr/td/h2").text
    author = driver.find_element_by_xpath(link2.format(2)).text
    publisher = driver.find_element_by_xpath(link2.format(3)).text
    year = driver.find_element_by_xpath(link2.format(7)).text
    price = driver.find_element_by_xpath(link2.format(8)).text
    genre = driver.find_element_by_xpath(link2.format(1)).text
    details = [title,genre,author,publisher,year,price]
    all_details.append(details)
    driver.back()
    driver.get(driver.current_url)
    i+=1

with open('noolulagam.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(all_details)
details.clear()
all_details.clear()
print(driver.current_url," Page Scraped ")

# scrap book details from noolulagam.com/books/2..* page
while True:
    try:
        driver.find_element_by_xpath("//a[contains(text(),'அடுத்த பக்கம்»')]").click()
    except NoSuchElementException:
        print("All Pages Scraped")
        break
    i=0
    driver.get(driver.current_url)
    rows = len(driver.find_elements_by_xpath("//div[@id='content']//h4"))
    while i<rows:
        link1="//div[@id='content']/table/tbody/tr[{0}]/td/table/tbody/tr[4]/td/table/tbody/tr[{1}]/td[3]/a"
        link2="//div[@id='content']/table/tbody/tr[{0}]/td/table/tbody/tr[4]/td/table/tbody/tr[{1}]/td[3]"
        title=driver.find_element_by_xpath("//div[@id='content']/table/tbody/tr[{0}]/td/table/tbody/tr/td/h4".format(i+2)).text
        genre=driver.find_element_by_xpath(link1.format(i+2,1)).text
        author=driver.find_element_by_xpath(link1.format(i+2,2)).text
        publisher=driver.find_element_by_xpath(link1.format(i+2,3)).text
        year=driver.find_element_by_xpath(link1.format(i+2,4)).text
        price=driver.find_element_by_xpath(link2.format(i+2,5)).text
        details = [title,genre,author,publisher,year,price]
        all_details.append(details)
        i+=1

    with open('noolulagam.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_details)
    print(driver.current_url," Page Scraped ")
    details.clear()
    all_details.clear()

driver.quit()
