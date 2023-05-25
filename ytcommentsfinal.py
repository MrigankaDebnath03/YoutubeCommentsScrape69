from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


login_url = input("Enter: ")
driver = webdriver.Chrome(options= options)
driver.maximize_window()
driver.get(login_url)
time.sleep(15)

previous_height = 0

while True:
    height = driver.execute_script("""
            function getActualHeight(){
                return Math.max(
                    Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                    Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                    Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                );
            }
            return getActualHeight()
        """)
    
    driver.execute_script(f"window.scrollTo({previous_height},{previous_height+300})")
    time.sleep(1)
    previous_height += 300

    if previous_height >= height:
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')

# driver.quit()

title_text = soup.select_one('#container h1')
print(title_text.text)

comments = soup.select("#content #content-text")
comment_list = [x.text for x in comments]

comment_list_final = [[x] for x in comment_list]
print(comment_list_final)

# driver.quit()

uname = soup.findAll('span',{"class":"style-scope ytd-comment-renderer"})
uname_final = [[x.text] for x in uname]

for i in uname:
    print(i.text)

with open('commentlist.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    # thewriter.writerows(comment_list_final)
    for value1, value2 in zip(comment_list_final, uname_final):
        thewriter.writerow([value1,value2])

