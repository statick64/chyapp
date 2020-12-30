from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database_helper import MemberDB,DatabaseHelper
import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class ChyBot:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    def go_to_login(self):
        bot.driver.find_element_by_xpath(
            "/html/body/div/header/div/div/div[1]/div/a[1]").click()

    def sign_in(self, username,password):
        self.driver.get("https://www.chymall.net/Mall/Login")
        self.driver.implicitly_wait(6)
        user_name = self.driver.find_element_by_xpath(
            "/html/body/div[1]/form/div/div[2]/ul/li[1]/input")
        user_password = self.driver.find_element_by_xpath(
            "/html/body/div[1]/form/div/div[2]/ul/li[2]/input")
        button = self.driver.find_element_by_xpath(
            "/html/body/div[1]/form/div/div[2]/button")
        user_name.click()
        user_name.send_keys(username)
        user_password.click()
        user_password.send_keys(password)
        button.click()

    def check_chy_point(self):
        hasLoaded = self.delay_url()
        if hasLoaded:
            self.driver.get("https://www.chymall.net/mall/UserCenter/Index")
            value = self.delay("/html/body/div/div[2]/div/div[1]/div/div[2]/div/form/ul/li[9]/input")
            text = value.get_attribute("value")
            return text

    def Vip(self):
        value = self.delay("/html/body/div/div[2]/div/div[1]/div/div[2]/div/form/ul/li[5]/input")
        text = value.get_attribute("value")
        return text


    def check_countdown(self):
        self.driver.get("https://www.chymall.net/mall/Order/MyOrder")
        value = self.delay("/html/body/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/p[2]")
        return value.text

    def delay_click(self,path):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, path))
        )
        return element
    def delay(self,path):
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        return element
    def delay_url(self):
        hasLoaded = WebDriverWait(self.driver, 30).until(
            EC.url_matches("https://chymall.net/")
        )
        return hasLoaded




sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=00,min=52)
bot = ChyBot()
d = DatabaseHelper()
members = d.get_members_credentials()

for member in members:
    bot.sign_in(member.user_name,member.password)
    member.chy_points =   bot.check_chy_point()
    member.vip = bot.Vip()
    member.cycles = bot.check_countdown()
    member.last_scraped = datetime.datetime.now()
    d.insert_member(member=member)
print("Scrapped")
    