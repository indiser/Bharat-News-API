import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import json

load_dotenv()

def process_and_push_to_db(news_data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    locations_path = os.path.join(BASE_DIR, "india_locations_cities.csv")

    if not os.path.exists(locations_path):
        print(f"❌ Error: Could not find '{locations_path}'.")
        return

    try:
        df_locations = pd.read_csv(locations_path)
    except Exception as e:
        print(f"❌ Error reading locations CSV: {e}")
        return

    # ACCEPT DATA FROM RAM DIRECTLY
    articles = news_data.get('articles', [])
    print(f"Loaded {len(articles)} articles into memory. Processing...")

    processed_articles = []
    for article in articles:
        t = article['title'] if article['title'] else ""
        d = article['description'] if article['description'] else ""
        searchable = f"{t} {d}".lower()
        display = t.strip()
        if display:
            processed_articles.append((searchable, display))

    def get_state_stats(row):
        state_name = str(row['State']).lower()
        valid_names = [state_name]
        cities_str = str(row['cities']) 
        if cities_str and cities_str != "nan":
            city_list = [c.strip().lower() for c in cities_str.split(',')]
            valid_names.extend([c for c in city_list if c])
            
        found_headlines = []
        for search_text, display_headline in processed_articles:
            for term in valid_names:
                if f" {term} " in f" {search_text} ":
                    if display_headline not in found_headlines:
                        found_headlines.append(display_headline)
                    break 
        
        count = len(found_headlines)
        # hover_text = "<br>".join([f"➤ {h}" for h in found_headlines]) if count > 0 else "No active news."
        if count > 0:
            hover_text = json.dumps(found_headlines) 
        else:
            hover_text = json.dumps([])
        return pd.Series([count, hover_text])

    print("Scanning headlines against States & Cities...")
    df_locations[['news_count', 'headlines']] = df_locations.apply(get_state_stats, axis=1)

    df_final = df_locations[df_locations['news_count'] > 0].copy()
    df_final.sort_values(by='news_count', ascending=False, inplace=True)

    if "cities" in df_final.columns:
        df_final.drop("cities", axis=1, inplace=True)

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("❌ CRITICAL: DATABASE_URL environment variable is missing.")
        return

    try:
        print("Connecting to Neon Database...")
        engine = create_engine(db_url)
        df_final.to_sql("heatmap_data", engine, if_exists="replace", index=False)
        print(f"✅ DONE. Successfully pushed {len(df_final)} active regions to Neon.")
    except Exception as e:
        print(f"❌ Database Error: {e}")
