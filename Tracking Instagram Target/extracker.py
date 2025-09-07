from selenium import webdriver
import time
import pandas as pd
import smtplib
from datetime import datetime

driver = webdriver.Chrome()

USERNAME = ""
PASSWORD = ""
EX_PROFILE = "" 
CSV_FILE = "ex_tracker_log.csv"
SENDER_EMAIL = ""
SENDER_PASS = ""
RECEIVER_EMAIL = "ke7inpimenta@gmail.com"

def clean_number(text):
    text = text.replace(",", "").strip()
    if "K" in text:
        return int(float(text.replace("K", "")) * 1000)
    elif "M" in text:
        return int(float(text.replace("M", "")) * 1000000)
    else:
        return int(text) if text.isdigit() else 0
    

def send_email(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    server.quit()

driver.get("https://www.instagram.com/accounts/login/")
driver.implicitly_wait(10)


username = driver.find_element("name", "username")
password = driver.find_element("name", "password")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

submit = driver.find_element("xpath", "//button[@type='submit']")
submit.click()
time.sleep(7)


driver.get(EX_PROFILE)
driver.implicitly_wait(7)


stats = driver.find_elements("css selector", "header section ul li span span")

post = stats[0].text if len(stats) > 0 else "0"
follower = stats[2].text if len(stats) > 2 else "0"
followin = stats[4].text if len(stats) > 4 else "0"

posts = clean_number(post)
followers = clean_number(follower)
following = clean_number(followin)

print("Posts:", posts)
print("Followers:", followers)
print("Following:", following)

try:
    df = pd.read_csv(CSV_FILE)
    previous_followers = df["Followers"].iloc[-1] if not df.empty else None
    previous_following = df["Following"].iloc[-1] if not df.empty else None
except:
    df = pd.DataFrame(columns=["Date", "Posts", "Followers", "Following"])
    previous_followers = None
    previous_following = None


new_row = [{
    "Date": datetime.now(),
    "Posts": posts,
    "Followers": followers,
    "Following": following
}]
df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
df.to_csv(CSV_FILE, index=False)

messages = []

if previous_followers is not None:
    diff_followers = followers - previous_followers
    if diff_followers < 0:
        messages.append(f"Bro, she lost {abs(diff_followers)} followers today, W for you.")
    elif diff_followers > 0:
        messages.append(f"Bro, she gained {diff_followers} followers today, stay salty.")
    else:
        messages.append("No change in her followers today, chill bro.")

if previous_following is not None:
    diff_following = following - previous_following
    if diff_following < 0:
        messages.append(f"She unfollowed {abs(diff_following)} people today.")
    elif diff_following > 0:
        messages.append(f"She followed {diff_following} new people today.")
    else:
        messages.append("No change in her following today.")

if messages:
    final_message = "\n".join(messages)
    print(final_message)
    send_email(final_message)
else:
    print("First run, no previous data.")

driver.quit()