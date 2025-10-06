import matplotlib.pyplot as plt
import feedparser #python library that reads RSS feeds (structured news/advisory data)
import pandas as pd #a data analysis library - helps organize data in tables (data frames)
from datetime import datetime #lets you handle timestamps and create filenames with today's date
# python -m venv .venv
# .\.venv\Scripts\activate
feedUrls = ["https://www.cisa.gov/cybersecurity-advisories/all.xml",#RSS feed URLs cyber news websites
            "https://www.darkreading.com/rss.xml",
            "https://feeds.feedburner.com/TheHackersNews",
            "https://www.bleepingcomputer.com/feed/"] 


keywords = ["financial", "bank", "investment", "wealth", "advisor"] #words to look for
filtered = [] #empty list that matches keywords

for url in feedUrls: 
    feed = feedparser.parse(url)
    print(f"Checking feed: {url}, found {len(feed.entries)} entries")
    
    for entry in feed.entries: #looks at each entry .get extracts field, if something is missing empty string is returned      
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        date = entry.get("published", "")

        content = (title + " " + summary).lower()
        
        if any(k in content for k in keywords): #matches to see if article is relevant, if true
            filtered.append({ #adds
                "source": feed.feed.get("title", url),
                "date": date,
                "title": title,
                "link": link,
                "summary": summary[:200]  #short summary
            })


data = pd.DataFrame(filtered) #turns filtered list into pandas dataframe

if not data.empty:
    filename = f"threat_feed_{datetime.now().strftime('%Y%m%d')}.csv"
    data.to_csv(filename, index=False)
    print(f"Saved {len(data)} results to {filename}")
else:
    print("No relevant financial sector threats found")

#converts date column to datetime
data["date"] = pd.to_datetime(data["date"], errors='coerce', utc=True)
#finds valid dates
dataValid = data.dropna(subset=['date'])

#plot number of articles per month
month = dataValid.groupby(dataValid["date"].dt.month).size()
month.plot(kind="bar", title="Threats per Month")
plt.xlabel("Month")
plt.ylabel("Number of Posts")
plt.show()

#pip freeze > requirements.txt