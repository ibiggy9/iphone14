from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import smtplib
from email.message import EmailMessage
import traceback
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


global file_path
global file_path2

def scrape():

    Sender_Email = "ibigford9@gmail.com"
    Reciever_Email = "ibigford9@gmail.com"
    Password = 'mbzrbrosqpxdaxeg'
    
    
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #fsf
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--window-size=400x1500")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36')
        driver = webdriver.Chrome(service=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        
        url = "https://www.apple.com/ca/shop/buy-iphone/iphone-14-pro/6.7-inch-display-128gb-space-black"
        driver.get(url)
        time.sleep(5)
        tradeinTest = driver.find_element_by_id("noTradeIn_label").click()
        
        '''
        tradein = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "noTradeIn"))
        )
        tradein.click()
        '''
        driver.get_screenshot_as_file("shoot.png") 
        applecareTest = driver.find_element_by_id("applecareplus_59_noapplecare_label").click()

        time.sleep(3)
        availability = driver.find_element_by_css_selector("#root > div.rf-bfe > div.rf-bfe-selectionarea > div.rf-bfe-summary-wrapper > div > div > div > div > div > div.rf-bfe-summary-grid > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > button").click()
        
        
        time.sleep(3)
        postcode = driver.find_element_by_css_selector('.rf-productlocator-form-textinput').send_keys("N2L0E3")
        
        driver.find_element_by_css_selector(".rf-productlocator-form-textinput").send_keys(Keys.RETURN)

        time.sleep(3)
        try:
            status = driver.find_element_by_css_selector('.rf-productlocator-suggestions')

            sendNote("ibigford9@gmail.com", status.text, )

            if "No iPhone 14 Pro Max models are" in status.text:
                print(True)
                sendNote("ibigford9@gmail.com", status.text, "Nothing")
            else:
                print("False")
                sendNote("ibigford9@gmail.com", status.text, "Get After it son!")
        except:
            sendNote("ibigford9@gmail.com", "error", "Error")
            pass

    except:
        traceback.print_exc()





# This function send an email
def sendNote(recipients, content, subject):
    print(recipients)
    password = 'nysmhzdxjcflnwju'
    Sender_Email = 'darepfapp@gmail.com'
    try:
        newMessage = EmailMessage()                         
        newMessage['Subject'] = subject
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = recipients                  
        newMessage.set_content(content) 
        

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(Sender_Email, password)              
            smtp.send_message(newMessage)
            smtp.close()
            print("email sent!")
        
    
    except:
        traceback.print_exc()

while True:
    scrape()
    time.sleep(300)