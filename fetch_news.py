import asyncio
import aiohttp
import feedparser
import json
import os
import sys

# List of Reliable RSS Feeds (India Specific)
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",       
    "https://feeds.feedburner.com/NDTV-LatestNews",
    "https://www.ndtv.com/rss/top-stories",                             
    "https://www.indiatoday.in/rss/1206584",                            
    "https://www.indiatoday.in/rss/1206578",
    "https://indianexpress.com/section/india/feed/",                    
    "https://www.thehindu.com/news/national/feeder/default.rss",         
    "https://indianexpress.com/feed/",
    "https://www.firstpost.com/commonfeeds/v1/mfp/rss/web-stories.xml",
    "https://www.business-standard.com/rss/latest.rss",
    "https://www.thetimesofbengal.com/feed/",
    "https://www.headlinesoftoday.com/feed/",
    "https://prod-qt-images.s3.amazonaws.com/production/thequint/feed.xml",
    "https://crowdwisdom.live/feed/",
    "https://newstodaynet.com/feed/",
    "https://www.opindia.com/feed/",
    "https://feeds.indiasnews.net/rss/701ee96610c884a6",
    "https://techgenyz.com/feed/",
    "https://news.abplive.com/home/feed",
    "https://apnlive.com/feed/",
    "https://thenewsmill.com/feed/",
    "https://prod-qt-images.s3.amazonaws.com/production/nationalherald/feed.xml",
    "https://prod-qt-images.s3.amazonaws.com/production/freepressjournal/feed.xml",
    "https://www.india.com/feed/",
    "https://tfipost.com/feed/",
    "https://www.thehindubusinessline.com/?service=rss",
    "https://thebetterindia.com/rss",
    "https://www.siasat.com/feed/",
    "https://www.oneindia.com/rss/news-india-fb.xml",
    "https://organiser.org/feed/",
    "https://news1india.in/feed/",
    "https://timesofindia.indiatimes.com/rssfeedmostrecent.cms",
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "https://feeds.feedburner.com/ndtvnews-top-stories",
    "https://feeds.feedburner.com/ndtvnews-latest",
    "https://feeds.feedburner.com/ndtvnews-india-news",
    "https://www.hindustantimes.com/feeds/rss/cities/kolkata-news/rssfeed.xml",
    "https://indianexpress.com/feed/",
    "https://www.thehindu.com/news/national/feeder/default.rss"
]

async def fetch_feed(session, url):
    """Fetches a single feed asynchronously and parses the text."""
    try:
        # A 10-second timeout ensures one dead server doesn't hang your pipeline
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                text = await response.text()
                
                # Parse the raw XML string asynchronously
                feed = feedparser.parse(text)
                
                if feed.bozo:
                    return []
                
                articles = []
                for entry in feed.entries:
                    title = entry.title if 'title' in entry else ""
                    description = entry.summary if 'summary' in entry else ""
                    articles.append({"title": title, "description": description})
                
                print(f"  -> Found {len(articles)} articles from {url}")
                return articles
            else:
                print(f"  Warning: {response.status} from {url}")
                return []
    except Exception as e:
        print(f"  Error connecting to {url}: {e}")
        return []

async def get_all_news():
    print(f"🚀 Concurrently fetching {len(RSS_FEEDS)} news feeds...")
    articles_list = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, url) for url in RSS_FEEDS]
        results = await asyncio.gather(*tasks)
        for result in results:
            articles_list.extend(result)

    # Return the data directly to RAM, do not save to disk
    print(f"✅ Fetched {len(articles_list)} articles.")
    return {"articles": articles_list}