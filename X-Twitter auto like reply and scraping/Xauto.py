from selenium import webdriver
import pandas as pd
import time



driver = webdriver.Chrome()

driver.get("https://x.com/i/flow/login")
driver.implicitly_wait(7)
USERNAME = ""
PASSWORD = ""
autolike = True          
autoreply = True  
tweets_to_reach = 5       
reply = "Nice work!" 
hashtags_toscrape = ["gym","ai","deeplearning"]

username = driver.find_element("xpath", "//input[@name='text']")
username.send_keys(USERNAME)
driver.implicitly_wait(7)


next_btn = driver.find_element("xpath", "//span[text()='Next']")
next_btn.click()
driver.implicitly_wait(7)

passw = driver.find_element("xpath", "//input[@name='password']")
passw.send_keys(PASSWORD)
driver.implicitly_wait(7)

login_btn = driver.find_element("xpath", "//span[text()='Log in']")
login_btn.click()
time.sleep(7)

data = []

for tags in hashtags_toscrape:
    driver.get(f"https://x.com/search?q=%23{tags}&src=typed_query&f=live")
    driver.implicitly_wait(7)

    tweetss = driver.find_elements("xpath","//div[@data-testid='cellInnerDiv']")[:tweets_to_reach]
    for tweets in tweetss:
        #twitter usrname
        try:
            try:
                profile_link = tweets.find_element("tag name", "a")  
                url = profile_link.get_attribute("href") 
                k = len("https://x.com/")
                Username = url[k:]
            except:
                Username = "N/A"


            try:
                tweeting = tweets.find_element("xpath",".//div[@data-testid='tweetText']")
                tweet = tweeting.text
            except:
                tweet = "N/A"
    
            try:       
                tweet_link = tweets.find_element("xpath", ".//a[contains(@href,'/status/')]")
                tweet_url = tweet_link.get_attribute("href")
            except:
                tweet_url = "N?A"

            if autolike:
                try:
                    #autolike
                    hh = tweets.find_element("xpath",".//button[@data-testid='like']")
                    hh.click()
                    time.sleep(2)
                    print("autolikedone")
                except:
                    ("autolike failed")
                    pass

            if autoreply:
                try:
                    # click reply button
                    reply_btn = tweets.find_element("xpath", ".//button[@data-testid='reply']")
                    reply_btn.click()
                    time.sleep(2)

                    # type reply
                    textarea = driver.find_element("xpath", "//div[@data-testid='tweetTextarea_0']")
                    textarea.send_keys(reply)
                    time.sleep(1)

                    # post reply
                    post_btn = driver.find_element("xpath", "//button[@data-testid='tweetButton']")
                    post_btn.click()
                    time.sleep(3)

                    print("Auto Reply Done ✅")
                except Exception as e:
                    print("Auto Reply Failed ❌", e)
                    pass
                        

            info = {
                        "Hashtag": tags,
                        "Handle": Username,
                        "Tweet": tweet,
                        "URL": tweet_url,
                    }
            data.append(info)
        except:
           data.append({
        "Hashtag": "Error",
        "Handle": "Error",
        "Tweet": "N/A",
        "URL": "N/A",
    })

  
df = pd.DataFrame(data)
df.to_csv("tweets.csv", index=False)

driver.quit()

















