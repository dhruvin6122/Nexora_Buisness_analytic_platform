import os
import logging
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

# Logger setup
logger = logging.getLogger(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

# Logger setup
logger = logging.getLogger(__name__)

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        database_url = os.getenv("NEON_DATABASE_URL")
        if not database_url:
            raise ValueError("NEON_DATABASE_URL environment variable is not set.")
        _engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True
        )
    return _engine

def get_session():
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

def get_db_connection() -> SQLDatabase:
    """
    Creates and returns a LangChain SQLDatabase instance connected to Neon Postgres.
    Restricted to the 'nexora_sales' schema.
    """
    try:
        # Create SQLAlchemy engine
        engine = get_engine()
        
        # Initialize SQLDatabase with schema restriction and sample rows enabled
        db = SQLDatabase(
            engine,
            schema="nexora_sales",
            include_tables=["customers", "products", "orders"],
            view_support=True,
            sample_rows_in_table_info=3
        )
        logger.info("Successfully connected to the database.")
        return db
    except Exception as e:
        raise

def get_dashboard_stats():
    """
    Fetches quick stats for the sidebar dashboard.
    Returns: dict with 'total_customers', 'today_revenue', 'today_orders'
    """
    from sqlalchemy import text
    session = get_session()
    stats = {}
    try:
        # Total Customers
        res_cust = session.execute(text("SELECT COUNT(*) FROM nexora_sales.customers")).scalar()
        stats['total_customers'] = res_cust or 0
        
        # Today's Revenue & Orders
        res_today = session.execute(text("""
            SELECT COUNT(*), COALESCE(SUM(total_amount), 0) 
            FROM nexora_sales.orders 
            WHERE DATE(order_date) = CURRENT_DATE
        """)).fetchone()
        
        stats['today_orders'] = res_today[0] if res_today else 0
        stats['today_revenue'] = float(res_today[1]) if res_today else 0.0
        
        return stats
    except Exception as e:
        logger.error(f"Stats Error: {e}")
        return {'total_customers': 0, 'today_revenue': 0, 'today_orders': 0}
    finally:
        session.close()
