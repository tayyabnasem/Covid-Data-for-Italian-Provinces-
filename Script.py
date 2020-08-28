from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
    driver = webdriver.Chrome("chromedriver.exe")
    province = input('Enter the province in Italy: ')
    url = "https://statistichecoronavirus.it/province-coronavirus-italia/"+province.lower()+"/"

    try:
        print('Getting total cases data...')
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        cases_element = soup.find('span', attrs={'class':'number'})
        total_cases = cases_element.text
        print('Province:',province,' Total Cases: ',total_cases)
        print('Fetching Articles links...')
        driver.get("https://www.google.com/")
        search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        search_term = 'Covid '+ province
        search.send_keys(search_term)
        search_btn = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
        search_btn.click()
        news_section = driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a')
        news_section.click()

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        articles_links = []
        print('Links for related Articles')
        for article in soup.find_all('div', attrs={'class': 'dbsr'}):
            link = article.find('a')['href']
            articles_links.append(link)
            print(link)

        dataframe = pd.DataFrame({'Cases':total_cases, 'Links': articles_links})
        dataframe.to_csv('province.csv', index=False, encoding='utf-8')
    except:
        print('Province name is not valid or there is a problem with the internet connection')

    driver.quit()

if __name__=='__main__':
    scrape_data()
