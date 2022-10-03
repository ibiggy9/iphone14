from urllib import response
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
import imghdr

#Where I store the screen shot that will be attached in the email
file_path = "/app/shoot.png"

count = 0
responses = []

#Main Scraping function
def scrape():
    Sender_Email = "myemail"
    Reciever_Email = "myemail"
    Password = 'myapppassword'
    
    
    # Convention for running selenium buildpack on Heroku
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #fsf
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=400x1500")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36')
        driver = webdriver.Chrome(service=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        
        url = "https://www.apple.com/ca/shop/buy-iphone/iphone-14-pro/6.7-inch-display-128gb-space-black"
        driver.get(url)
        time.sleep(5)
        tradeinTest = driver.find_element(By.ID,"noTradeIn_label").click()
        
        '''
        tradein = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "noTradeIn"))
        )
        tradein.click()
        '''
        driver.get_screenshot_as_file("shoot.png") 
        applecareTest = driver.find_element(By.ID, "applecareplus_59_noapplecare_label").click()

        time.sleep(3)
        try:
            print(count)
            checkOn = driver.find_element(By.CSS_SELECTOR, ".rf-pickup-quote-value")
            driver.get_screenshot_as_file("/app/shoot.png")
            print(checkOn.text)
            if checkOn.text == 'Check availability from 16/09':
                count + 1
            
            else:
                sendNote("myemail", "Check the website now", "Check the website now!")
                
            
            if count%1000 == 0:
                sendNote("myemail", checkOn.text, "No Change Yet!")

        except:
            error = traceback.print_exc()
            sendNote("myemail", error, "Error")
            pass
            

        time.sleep(3)
    
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
        with open(file_path, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(Sender_Email, password)              
            smtp.send_message(newMessage)
            smtp.close()
            print("email sent!")
        
    
    except:
        traceback.print_exc()

# run every 300 seconds
while True:
    scrape()
    time.sleep(300)
