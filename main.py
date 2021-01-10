import json
import os
import sys
import time
from getpass import getpass

import selenium
import twocaptcha
from datetime import datetime
from colorama import Fore, init
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha

init(autoreset=True)
print(Fore.LIGHTCYAN_EX + "AutoCheckBand v0.1")


def Debug(Object):
    Debug = driver.execute_script(
        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
        Object)
    return Debug


def solveCaptcha(SeleniumDriver, APIKEY, Debug=False):
    """Captcha = driver.find_element_by_xpath(Paths["Captcha"]).text
    print(Captcha)"""
    st = time.time()
    print("Solving Captcha...")
    solver = TwoCaptcha(APIKEY)
    try:
        balance = solver.balance()
        if balance == 0:
            print(Fore.RED + "Account Balance is 0")
            driver.quit()
            sys.exit()
    except twocaptcha.api.ApiException:
        print(Fore.RED + "Invalid 2Captcha APIKEY")
        driver.quit()
        sys.exit()

    def get_sitekey(SeleniumDriver):
        return SeleniumDriver.find_element_by_class_name("g-recaptcha").get_attribute(
            "data-sitekey"
        )

    def form_submit(SeleniumDriver, token):
        SeleniumDriver.execute_script("token='" + token + "'")
        SeleniumDriver.execute_script("document.getElementById(\"g-recaptcha-response\").innerHTML=token")
        SeleniumDriver.execute_script("_grecaptchaCallback(token)")
        time.sleep(1)

    result = solver.recaptcha(sitekey=get_sitekey(SeleniumDriver),
                              url=SeleniumDriver.current_url,
                              version="v2")
    if not Debug:
        form_submit(SeleniumDriver, result["code"])
        print("Captcha Solved, Takes " + str(time.time() - st) + " seconds")
    elif Debug:
        return result


def login(SeleniumDriver, UserAuthInfo):
    SeleniumDriver.get(Urls["FastEmail"])
    # Submit Email
    try:
        WebDriverWait(SeleniumDriver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "uTitH1"))
        )
        mailbox = SeleniumDriver.find_element_by_xpath(Paths["LoginEmailTextArea"])
        mailbox.send_keys(UserAuthInfo["ID"])
        submitButton = SeleniumDriver.find_element_by_xpath(Paths["LoginSubmitButton"])
        try:
            submitButton.click()
        except ElementClickInterceptedException:
            print(Fore.RED + "Invalid Email")
            driver.quit()
            sys.exit()
        try:
            WebDriverWait(SeleniumDriver, 1).until(EC.alert_is_present())
            alert = SeleniumDriver.switch_to.alert
            alert.accept()
            print(Fore.RED + "Invalid Email")
            driver.quit()
            sys.exit()
        except TimeoutException:
            pass
    finally:
        pass
    # Submit Password
    try:
        WebDriverWait(SeleniumDriver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "uTitH1"))
        )
        mailbox = SeleniumDriver.find_element_by_xpath(Paths["LoginPasswordTextArea"])
        mailbox.send_keys(UserAuthInfo["PW"])
        submitButton = SeleniumDriver.find_element_by_xpath(Paths["LoginSubmitButton"])
        try:
            submitButton.click()
        except ElementClickInterceptedException:
            print(Fore.RED + "Invalid Password")
            driver.quit()
            sys.exit()
        if not SeleniumDriver.current_url == "https://band.us":
            try:
                WebDriverWait(SeleniumDriver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["FeedButton"])))
            except TimeoutException:
                solveCaptcha(driver, UserAuthInfo["APIKEY"])
        try:
            WebDriverWait(SeleniumDriver, 1).until(EC.visibility_of_element_located((By.XPATH, Paths["LoginNotPass"])))
            print(Fore.RED + "Invalid Password")
            driver.quit()
            sys.exit()
        except TimeoutException:
            print(Fore.LIGHTGREEN_EX + "Login Successful")
            pass
    finally:
        pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = BASE_DIR.replace("\\", "/")
options = selenium.webdriver.ChromeOptions()
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
options.add_argument("log-level=3")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36")
options.add_argument("headless")
options.add_argument("window-size=7680x4320")
options.add_argument("lang=ko_KR")
# options.add_extension("SomeExtension.crx")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path=BASE_DIR + "/Driver.exe")
Section = 1
SleepTime = 3
if not os.path.isdir("data"):
    os.mkdir("data")
Paths = {"MainLoginButton": "/html/body/div[1]/div/header/div/div/a[2]",
         "LoginEmailLoginButton": """//*[@id="email_login_a"]/span""",
         "LoginEmailTextArea": "/html/body/div/section/form/div/div/div/input",
         "LoginPasswordTextArea": "/html/body/div/section/form/div/div[2]/div/input",
         "LoginSubmitButton": "/html/body/div/section/form/button",
         "LoginNotPass": "/html/body/div/section/form/div/div[2]/p",
         "Captcha": "/html/body/div[2]/div",
         "CaptchaTextArea": "/html/body/div[2]/div/div/textarea",
         "FeedButton": "/html/body/div[1]/header/div[2]/ul/li[1]/a",
         "FirstBandLink": "/html/body/div[1]/div[1]/main/div/div[2]/div/section[" + str(Section) +
                          "]/section/div/div/h2/a",
         "CheckPath": "/html/body/div[1]/div[1]/main/div/div[2]/div/section[" + str(Section) +
                      "]/section/div/div/section",
         "Checker": "/html/body/div[1]/div[1]/main/div/div[2]/div/section[" + str(Section) +
                    "]/section/div/div/section/div/div[2]/div[2]/div/div[2]",
         "Checker2": "/html/body/div[1]/div[1]/main/div/div[2]/div/section[" + str(Section) +
                     "]/section/div/div/section/div/div[2]/div[2]/div/div[1]",
         "ExpectedButton": "/html/body/div[1]/div[3]/div/div/section/div[2]/div/section/div/div[4]/div[3]/"
                           "div[2]/div/div[2]/ul/li[1]/div/label/span/input",
         "ExpectedButton2": "/html/body/div[1]/div[3]/div/div/section/div[2]/div/section/div/div[4]/div[3]/"
                            "div/div/div[2]/ul/li[1]/div/label/span/input",
         "PostTime": "/html/body/div[1]/div[3]/div/div/section/div[2]/div/section/div/div[3]/div/div/a/time"}
Urls = {"Main": "https://band.us",
        "FastEmail": "https://auth.band.us/email_login?keep_login=false"}
if os.path.isfile("Auth.json"):
    print(Fore.LIGHTBLUE_EX + "Use Already Exist Account...")
    with open("Auth.json", "r", encoding="utf-8") as File:
        AuthInfo = json.loads(File.read())
    login(driver, AuthInfo)
else:
    print(Fore.LIGHTBLUE_EX + "Use New Account...")
    print(Fore.LIGHTYELLOW_EX + "Validating Account Info...")
    AuthInfo = {"ID": str(input("Email : ")),
                "PW": str(getpass("Password : ")),
                "BANDID": str(input("Band Id : ")),
                "APIKEY": str(getpass("2Captcha Api Key : "))}
    login(driver, AuthInfo)
    print(Fore.LIGHTGREEN_EX + "Checked Account Info!")
    with open("Auth.json", "w", encoding="utf-8") as File:
        File.write(json.dumps(AuthInfo))

FeedButton = driver.find_element_by_xpath(Paths["FeedButton"])
FeedButton.click()

PostTime = []
PostType = None
while True:
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["FirstBandLink"])))
    BandLinkId = driver.find_element_by_xpath(Paths["FirstBandLink"]).get_attribute("href").split("/")[4]
    if BandLinkId == AuthInfo["BANDID"]:
        try:
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["Checker"])))
                PChecker = driver.find_element_by_xpath(Paths["Checker"])
                PostType = 1
            except TimeoutException:
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["Checker2"])))
                    PChecker = driver.find_element_by_xpath(Paths["Checker2"])
                    PostType = 2
                except TimeoutException:
                    raise TimeoutException
            BandWindowCreate = driver.find_element_by_xpath(Paths["CheckPath"])
            BandWindowCreate.click()
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["PostTime"])))
            PTime = driver.find_element_by_xpath(Paths["PostTime"])
            if PTime.text not in PostTime:
                PostTime.append(PTime.text)
                if PostType == 1:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["ExpectedButton"])))
                    CheckButton = driver.find_element_by_xpath(Paths["ExpectedButton"])
                    if CheckButton.is_selected():
                        print("Found New Attendance but Already Checked")
                    else:
                        CheckButton.click()
                        print("Checked!")
                elif PostType == 2:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, Paths["ExpectedButton2"])))
                    CheckButton = driver.find_element_by_xpath(Paths["ExpectedButton2"])
                    if CheckButton.is_selected():
                        print("Found New Attendance but Already Checked")
                    else:
                        CheckButton.click()
                        print("Checked!")
                else:
                    print("ERROR")
                driver.save_screenshot(BASE_DIR + "/data/" + str(datetime.now().isoformat()).replace(":", "_") + ".png")
            else:
                pass
        except TimeoutException:
            pass
    else:
        pass
    time.sleep(SleepTime)
    driver.refresh()
