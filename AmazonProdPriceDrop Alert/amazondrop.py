from selenium import webdriver
from datetime import datetime
import pandas as pd
import smtplib

url = "https://www.amazon.in/Alienware-Area-51-Gaming-Desktop-Service/dp/B0FG379545/ref=sr_1_4?dib=eyJ2IjoiMSJ9.QGA0mq6lOiy2-xsfB62WBVbEnF0t7SPJOeKhwzao1WlWVDOR49C8DpbbzMvWvBuJkKf8oKyrXMhUyDFnUxcBw74IpR0Ghx1lm1Pw6lQ_WAxeNDJUOwZhcKzf0s7lfw5-prq7rBLkqjB08nH-63k9ZWh94vSN0hji7kuXJm77Cz_qxm2EatXRqB-9o3rgbtEtTfPE-3ZU-hgb6tmYrPn85yxROKSzl_8P1C1qWOTPgj4.zd21m73nH58f5pbgrKRmLNSeGBXfkRgmiWSeuRM1VbU&dib_tag=se&keywords=gaming&qid=1757191281&sr=8-4"
CSV_FILE = "amazon_price_log.csv"                     
SENDER_EMAIL = "botwebscrapinggg@gmail.com"
SENDER_PASS = ""
RECEIVER_EMAIL = "ke7inpimenta@gmail.com"                  



driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(7)


try:
    item_name = driver.find_element("css selector","#productTitle")
    item = item_name.text
except:
    item = "N/A"

message = f"Price dropped! 🎉 Check your product: {item}"

try:
    item_price = driver.find_element("xpath","//span[@class='a-price-whole']")
    price = int(item_price.text.replace(",",""))
except:
    price = "N/A"

print(f"Current Price: ₹{price}")


try:
    df = pd.read_csv(CSV_FILE)
    previous_price = df["Price"].iloc[-1] if not df.empty else None
except:
    df = pd.DataFrame(columns=["Date","Item","Price"])
    previous_price = None

new_row = [{
    "Date": datetime.now(),
    "Item": item,
    "Price": price
}]

df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)

def send_email(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    server.quit()

if previous_price and price < previous_price:
    print(f"Price dropped from ₹{previous_price} to ₹{price}! Sending WhatsApp alert...")
    now = datetime.now()
    send_email(message)
else:
    now = datetime.now()
    print("Price did not drop compared to last check.")
    




