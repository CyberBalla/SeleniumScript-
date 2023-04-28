import os
import time
import random
import string
import logging
from os import path
import logging.config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

### CONSTANTS
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
ACCOUNTS = 100


### setup logger and get root logger
log_config_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_config_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__) 


"""
    getRandomString
"""
def getRandomString(length):
    result_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    return result_str


"""
    waitForElementToBeLocated
    @param driver
    @param locator
    @param locatorType
    @param timeout
    @param poolFrequency
    @return {webdriver} element
"""
def waitForElementToBeLocated(driver, locator, locatorType=By.XPATH, timeout=10, pollFrequency=0.5):
    element = None
    try:
        # logger.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element with locator :: " + locator + " :: to be visible")
        wait = WebDriverWait(driver, timeout, poll_frequency=pollFrequency,
                                ignored_exceptions=[NoSuchElementException,
                                                    ElementNotVisibleException,
                                                    ElementNotSelectableException])
        element = wait.until(EC.presence_of_element_located((locatorType, locator)))
        # logger.info("Found!")
    except:
        logger.info("Warning :: Element with locator: "+ locator +" NOT appeared on the web page")
    return element


"""
    registerAccounts
"""
def registerAccounts():
    ### init chromedriver
    # service = Service(os.environ.get("CHROME_DRIVER_PATH"))
    service = Service(ChromeDriverManager().install())
    options = Options()
    # options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    i = 0
    while i < ACCOUNTS:
        try:
            i += 1
            
            # generate random name, email, password
            name = getRandomString(12)+str(i)
            email = name + "@gmail.com"
            password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))

            logger.info("----------------------------")
            logger.info(f"name: {name}")
            logger.info(f"email: {email}")
            logger.info(f"password: {password}")
            
            # get register url
            BASE_URL = "https://password-vault-test.netlify.app"
            driver.get(f"{BASE_URL}/register")
            time.sleep(5)

            # register user
            elName = waitForElementToBeLocated(driver, '//input[@id="name"]')
            elName.send_keys(name)

            elEmail = driver.find_element(By.XPATH, '//input[@id="email"]')
            elEmail.send_keys(email)

            elPass = driver.find_element(By.XPATH, '//input[@id="password"]')
            elPass.send_keys(password)

            elConfirmPass = driver.find_element(By.XPATH, '//input[@id="confirm-password"]')
            elConfirmPass.send_keys(password)

            elBtnCreate = driver.find_element(By.XPATH, '//button[contains(text(), "Create")]')
            elBtnCreate.send_keys(Keys.RETURN)
            time.sleep(5)

            #### STORE User
            elAddPassword = waitForElementToBeLocated(driver, '//button[contains(text(), "Add Password")]')
            elAddPassword.click()

            elWebsiteInput = waitForElementToBeLocated(driver, '//input[@name="website"]')
            elWebsiteInput.send_keys(BASE_URL)

            elNameInput = waitForElementToBeLocated(driver, '//input[@name="login"]')
            elNameInput.send_keys(email)

            elPasswordInput = waitForElementToBeLocated(driver, '//input[@name="password"]')
            elPasswordInput.send_keys(password)

            elSaveBtn = driver.find_element(By.XPATH, '//button[contains(text(), "Save")]')
            elSaveBtn.click()
            time.sleep(5)

            elBtnLogout = waitForElementToBeLocated(driver, '//button[contains(text(), "Logout")]')
            elBtnLogout.click()
            time.sleep(3)
            logger.info("Account Created")
        
        except Exception as e:
            logger.error(f"Error: {e}")
            driver.delete_all_cookies()
            driver.refresh()
            time.sleep(2)
            continue

    driver.quit()

if __name__ == "__main__":
    response = registerAccounts()