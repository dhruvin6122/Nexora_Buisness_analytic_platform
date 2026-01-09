from fastapi import APIRouter, HTTPException
from backend.db import get_dashboard_stats
from backend.schemas import DashboardStats

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
def get_stats():
    try:
        stats = get_dashboard_stats()
        return DashboardStats(
            today_orders=stats.get('today_orders', 0),
            today_revenue=stats.get('today_revenue', 0.0),
            total_customers=stats.get('total_customers', 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
