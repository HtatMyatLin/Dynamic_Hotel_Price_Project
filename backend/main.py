from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db

app = FastAPI(
    title="AI Hotel Pricing Support API",
    description="Member 6 Backend - Kamata Hotel Dynamic Pricing Prototype",
    version="0.1.0"
)

# Allow Member 7's frontend to call this API without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on FastAPI startup."""
    init_db()

@app.get("/")
def health_check():
    return {"status": "ok", "member": "M6", "branch": "backend/fastapi-setup"}

# Week 1 Deliverable: Return 1 mock record so Member 7 can render the UI
@app.get("/api/v1/sample-hotel")
def get_sample_hotel():
    return {
        "data_kind": "SAMPLE",
        "dataset_version": "w1-mock-v1",
        "stay_date": "2026-12-05",
        "room_group": "SINGLE_NON_SMOKING",
        "adults": 1,
        "nights": 1,
        "meal_plan": "ROOM_ONLY",
        "own_hotel": {
            "hotel_id": "OWN_01",
            "hotel_name": "ホテル オリエンタル エクスプレス 東京蒲田 (サンプル)",
            "sales_status": "ON_SALE",
            "current_price_yen": 14500,
            "recommended_price_yen": 15900,
            "reason_ja": "比較可能な3施設の中央値は15,800円です。稼働率とイベントの設定を加味しましたが、変更幅の上限により15,900円を参考提案します。これはサンプルデータによる結果です。"
        },
        "competitors": [
            {
                "hotel_id": "COMP_01",
                "hotel_name": "競合ホテルA (蒲田駅東口)",
                "price_yen": 15800,
                "source_url": "https://example.com/hotel-a",
                "collected_at": "2026-11-25T14:00:00+09:00"
            }
        ]
    }