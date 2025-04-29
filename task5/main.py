import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from database import Database


app = FastAPI(
    title="URL Saver API",
    description="API for saving URLs to database",
)

db = Database()

@app.get("/save_url", summary="Save URL to database")
async def save_url(
    url: str = Query(..., description="URL to save"),
):
    try:
        # Создаем mock продукта с URL
        mock_product = {
            "name": "Saved URL",
            "type": "url",
            "price": "0",
            "rating": "0",
            "reviews": "0",
            "link": url
        }
        
        db.save_products([mock_product])
        return {
            "status": "success",
            "message": f"URL {url} saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_urls", summary="Get all URLs from database")
async def get_urls(
    limit: int = Query(10, description="Quantity of URLs", ge=1)
):
    try:
        products = db.get_products(limit)
        # Возвращаем только URLs
        return [{"url": product["link"], "saved_at": product["parse_date"]} for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)