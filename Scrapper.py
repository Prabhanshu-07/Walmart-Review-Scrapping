from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
df = pd.DataFrame(columns=['Review_date','Review_name','Review_title','Review_description','Rating_outof_5'])
dates=[]
names=[]
titles=[]
descriptions=[]
ratings=[]
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365")
driver.implicitly_wait(10)
reviews = driver.find_element(By.XPATH, '//*[@id="customer-reviews-header"]/div[2]/div/div[3]/a[2]/span')
driver.execute_script("arguments[0].scrollIntoView();",reviews)
reviews.click()
recent_reviews= driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[5]/div/div[2]/div/div[2]/div/div[2]/select/option[3]')
recent_reviews.click()
driver.refresh()
date=True

while date:
    a=True
    for x in range(2,23):
        if x<6:
             n=x
        elif x>5:
             n=5
        body = driver.find_elements_by_xpath("//*[@class='review-text']")
        for i,txt in enumerate(body):
            descriptions.append(txt.text)
            try:
                titles.append(driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{i+1}]/div/div[1]/div/div[1]/div[1]/h3").text)
            except NoSuchElementException:
                titles.append('NA')
            ratings.append(driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{i+1}]/div/div[1]/div/div[1]/div[1]/div/div/span[3]/span[2]").text)
        name = driver.find_elements_by_xpath("//*[@class='review-footer-userNickname']")
        for post in name:
            names.append(post.text)
        dat = driver.find_elements_by_xpath("//*[@class='review-date-submissionTime']")
        for wr in dat:
            date=wr.text.split()[0]
            if date=='December':
                a=False
                break
            dates.append(wr.text)
        date=a
        if date==False and a ==False:
            break
        driver.find_element_by_xpath(f"/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[2]/div/div/ul/li[{n}]/button").click()
        driver.refresh()



df["Review_date"]=dates
df["Review_name"]=names
df["Review_title"]=titles
df["Review_description"]=descriptions
df["Rating_outof_5"]=ratings
driver.quit()
df.to_csv('output.csv')









