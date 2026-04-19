import asyncio
from dotenv import load_dotenv

# Import your native RAM functions
from fetch_news import get_all_news
from process_data_india import process_and_push_to_db

# Ensure your .env file has the NEW database URL loaded
load_dotenv()

async def seed_database():
    print("🌱 Booting up the seeder...")
    try:
        print("1. Fetching fresh news into RAM...")
        news_data = await get_all_news()
        
        print("\n2. Processing and pushing to new Neon Database...")
        process_and_push_to_db(news_data)
        
        print("\n✅ Seeding complete. The table 'heatmap_data' now exists.")
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")

if __name__ == "__main__":
    asyncio.run(seed_database())