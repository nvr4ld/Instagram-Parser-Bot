from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from selenium.common.exceptions import NoSuchElementException

class Instagram():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.acc = acc
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def closeBrowser(self):
        self.driver.close()
        self.driver.quit()

    def login(self):

        driver = self.driver
        driver.get("https://www.instagram.com")

        time.sleep(4)

        username_inp = driver.find_element(By.NAME, "username")
        username_inp.clear()
        username_inp.send_keys(username)

        time.sleep(0.5)

        pw_inp = driver.find_element(By.NAME, "password")
        pw_inp.clear()
        pw_inp.send_keys(password)
        
        pw_inp.send_keys(Keys.ENTER)
        time.sleep(5)

    def getPhotos(self, acc):
        driver = self.driver
        driver.get("https://www.instagram.com/" + acc)
        time.sleep(2)

        posts = []
        posts_cnt = int(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span").text)
        loops = int(posts_cnt/12)
        for i in range(loops+1):
            all_hrefs = driver.find_elements(By.TAG_NAME, "a")
            posts_hrefs = [i.get_attribute("href") for i in all_hrefs if "/p/" in i.get_attribute("href")]

            for item in posts_hrefs:
                posts.append(item)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

        file_name = acc
        time.sleep(2)
        posts = list(set(posts))
        with open(f'{file_name}.txt', 'a') as file:
            for url in posts:
                file.write(url + '\n')
        return posts

    def downloadPhotos(self, acc):
        self.getPhotos(acc)
        driver = self.driver
        with open(f'{acc}.txt') as file:
            posts = list(set(file.readlines()))
            for i in posts:
                driver.get(i)
                time.sleep(2)
                file_name = i.split("/")[-2]
                try:
                # if self.xpathExists(soloimg_src):
                    img_parent = driver.find_element(By.CLASS_NAME, "_aagv")
                    img_url = img_parent.find_element(By.TAG_NAME, "img").get_attribute("src")
                    response = requests.get(img_url)
                    with open(f"{file_name}_img.jpg", "wb") as file:
                        file.write(response.content)
                    # time.sleep(1)         
                except NoSuchElementException:
                    continue


print ("Type your username:")
username = input()
print ("Type your password:")
password = input()
print ("Type account you would like to download photos from:")
acc = input()

nurBot = Instagram(username, password)

nurBot.login()
nurBot.downloadPhotos(acc)
nurBot.closeBrowser()


        
                