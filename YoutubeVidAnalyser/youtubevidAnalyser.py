import pandas as pd
from selenium import webdriver
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

url = "https://www.youtube.com/watch?v=vylke4pLqlI" #url of video
maxx = 100 #no.of comments to analyse
data = []
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

driver.execute_script("window.scrollTo(0, 800);")
time.sleep(2)


comments_seen = set()

analyzer = SentimentIntensityAnalyzer()
pos = 0
neg = 0
neu = 0
try:
    while len(data) < maxx:
        comments = driver.find_elements("css selector", "ytd-comment-thread-renderer")
        for comment in comments:
            try:
                content = comment.find_element("css selector", "#content-text span").text
                author = comment.find_element("css selector", "#author-text span").text.strip()

                if content in comments_seen:
                    continue
                comments_seen.add(content)

                score = analyzer.polarity_scores(content)
                if score["compound"] >= 0.05:
                    sentiment = "positive"
                    pos += 1
                elif score["compound"] <= - 0.05:
                    sentiment = "negative"
                    neg += 1
                else:
                    sentiment = "neutral"
                    neu += 1
                info = {
                    "Author": author ,
                    "Comment":content,
                    "Sentiment": sentiment
                }
                data.append(info)

                if len(data)>=maxx:
                    break
            except:
                continue

        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)


except Exception as e:
    print("Error:", e)

df = pd.DataFrame(data)
df.to_csv("youtube_comments.csv", index=False)

if max(pos,neg,neu) == pos:
    print("People like your video")
elif max(pos,neg,neu) == neg:
    print("Your video is Trash")
else:
    print("Your Video is Neutral")

print("Positive:",pos)
print("Negative:",neg)
print("Neutral:",neu)
    
driver.quit()


        


        
            









