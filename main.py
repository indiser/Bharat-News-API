from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from sqlalchemy import create_engine
import json
from fetch_news import get_all_news
from process_data_india import process_and_push_to_db

app = FastAPI(
    title="Internal Bharat News API", 
    description="Serverless API for fetching processed Indian heatmap data."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bharat News API is live Go to '/api/news' or '/api/news/state_code' . Hit /docs for documentation."}


@app.get("/api/news")
async def get_news():
    """Serves the latest heatmap data with clean, structured arrays."""
    try:
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            raise HTTPException(status_code=500, detail="Database not configured.")
            
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM heatmap_data", engine)
        df.fillna("", inplace=True)
        
        records = df.to_dict(orient='records')
        
        # Unpack the JSON strings back into native arrays
        for record in records:
            try:
                record['headlines'] = json.loads(record['headlines'])
            except:
                record['headlines'] = []
                
        return records
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news/{state_code}")
async def get_news_by_state(state_code: str):
    """Fetch news for a specific state using its 2-letter code."""
    try:
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            raise HTTPException(status_code=500, detail="Database not configured.")
            
        engine = create_engine(db_url)
        query = 'SELECT * FROM heatmap_data WHERE "Code" = %(state_code)s'
        df = pd.read_sql(query, engine, params={"state_code": state_code.upper()})
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No news found for state code: {state_code.upper()}")
            
        df.fillna("", inplace=True)
        
        # 1. Extract the single dictionary
        record = df.to_dict(orient='records')[0] 
        
        # 2. Unpack the stringified database column back into a real Python list
        try:
            record['headlines'] = json.loads(record['headlines'])
        except:
            record['headlines'] = []
            
        # 3. Return the clean object
        return record 
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cron/update")
async def trigger_update(authorization: str = Header(None)):
    """Vercel Cron hits this endpoint every hour to refresh the database."""
    expected_secret = os.environ.get("CRON_SECRET")
    if not authorization or authorization != f"Bearer {expected_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized.")

    try:
        print("🚀 Serverless Cron triggered. Fetching news...")
        news_data = await get_all_news()
        process_and_push_to_db(news_data)
        return {"status": "success", "message": "Database updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")