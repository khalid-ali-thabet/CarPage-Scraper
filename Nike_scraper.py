from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd 
import time 

driver = webdriver.Chrome('C:/chromedriver.exe')
driver.maximize_window()
driver.get('https://www.nike.com/ca/w/sale-3yaep')

last_heaight = driver.execute_script('return document.body.scrollHeight')


# general in any infinite scrolling sites 
while True:
    try:
        driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/button/svg').click()
    except:
        pass
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if last_heaight == new_height:
        break
    else:
        last_heaight = new_height
        
        
# makeing the data frame 
df = pd.DataFrame({'name':[''], 'subtitle':[''], 'full price':[''], 'sale price':[''], 'link':['']})

# start grapping 
soup = BeautifulSoup(driver.page_source, 'lxml')
products_cards = soup.find_all('div', class_ = 'product-card__body')


for product in products_cards:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        name = product.find('div', class_ = 'product-card__title').text
        subtitle = product.find('div', class_ = 'product-card__subtitle').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-1ydfahe').text 
        full_price = product.find('div', class_ ='product-price ca__styling is--striked-out css-0').text
        
        df = df.append({'name':name, 'subtitle':subtitle, 'full price':full_price, 'sale price':sale_price, 'link':link}, ignore_index=True)
    except:
        pass 
     
df.to_csv('D:/project2.csv')