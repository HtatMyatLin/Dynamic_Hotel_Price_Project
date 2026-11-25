"""
SQLAlchemy models for database tables.
Week 2: Database models matching the API contract.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Text

from backend.database import Base


class Hotel(Base):
    """Hotels table - both own hotel and competitor hotels."""
    __tablename__ = "hotels"

    hotel_id = Column(String(50), primary_key=True, index=True)
    hotel_name = Column(String(200), nullable=False)
    hotel_name_en = Column(String(200), nullable=True)
    hotel_address = Column(String(300), nullable=True)
    hotel_distance_meters = Column(Integer, nullable=True)
    is_own_hotel = Column(Boolean, default=False, nullable=False)
    sales_status = Column(String(20), default="ON_SALE")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Hotel(hotel_id="'{self.hotel_id}', name="'{self.hotel_name}')>"


class CompetitorPrice(Base):
    """Competitor hotel prices."""
    __tablename__ = "competitor_prices"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(String(50), nullable=False)
    stay_date = Column(Date, nullable=False, index=True)
    room_group = Column(String(50), nullable=False)
    adults = Column(Integer, nullable=False)
    nights = Column(Integer, nullable=False)
    meal_plan = Column(String(50), nullable=False)
    price_yen = Column(Integer, nullable=True)
    source_url = Column(String(500), nullable=True)
    source = Column(String(20), nullable=False)
    collected_at = Column(DateTime, nullable=False)
    missing_reason = Column(String(200), nullable=True)
    data_kind = Column(String(20), default="PUBLIC")
    dataset_version = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<CompetitorPrice(stay_date="'{self.stay_date}', hotel_id="'{self.hotel_id}', price={self.price_yen})>"

class Event(Base):
    """Local events affecting hotel pricing."""
    __tablename__ = "events"

    event_id = Column(String(50), primary_key=True, index=True)
    event_name = Column(String(200), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_date = Column(Date, nullable=False, index=True)
    impact_level = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Event(event_id="'{self.event_id}', name="'{self.event_name}')>"


class ImportHistory(Base):
    """CSV import operation history for audit."""
    __tablename__ = "import_history"

    import_id = Column(String(50), primary_key=True, index=True)
    filename = Column(String(200), nullable=False)
    target_table = Column(String(50), nullable=False)
    data_kind = Column(String(20), nullable=False)
    row_count = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    imported_at = Column(DateTime, nullable=False)
    error_row = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ImportHistory(import_id="'{self.import_id}', status="'{self.status}')>"


class PriceProposal(Base):
    """AI price recommendation proposals."""
    __tablename__ = "price_proposals"

    proposal_id = Column(String(50), primary_key=True, index=True)
    stay_date = Column(Date, nullable=False, index=True)
    room_group = Column(String(50), nullable=False)
    adults = Column(Integer, nullable=False)
    nights = Column(Integer, nullable=False)
    meal_plan = Column(String(50), nullable=False)
    own_hotel_price = Column(Integer, nullable=True)
    recommended_price = Column(Integer, nullable=True)
    median_price = Column(Integer, nullable=True)
    breakdown = Column(Text, nullable=True)
    hold_reasons = Column(Text, nullable=True)
    rule_version = Column(String(50), nullable=False)
    valid_until = Column(DateTime, nullable=False)
    data_kind = Column(String(20), default="PUBLIC")
    dataset_version = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<PriceProposal(proposal_id="'{self.proposal_id}', stay_date="'{self.stay_date}')>"


class StaffDecision(Base):
    """Staff decisions on price proposals - preserved for audit."""
    __tablename__ = "staff_decisions"

    decision_id = Column(String(50), primary_key=True, index=True)
    proposal_id = Column(String(50), nullable=False, index=True)
    decision = Column(String(20), nullable=False)
    final_price_yen = Column(Integer, nullable=True)
    reason = Column(Text, nullable=True)
    decided_by = Column(String(50), nullable=False)
    decided_at = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<StaffDecision(decision_id="'{self.decision_id}', proposal_id="'{self.proposal_id}')>"


class DailyCalendarStatus(Base):
    """Pre-computed daily calendar statuses for performance."""
    __tablename__ = "daily_calendar_status"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    room_group = Column(String(50), nullable=False, index=True)
    sales_status = Column(String(20), default="ON_SALE")
    current_price_yen = Column(Integer, nullable=True)
    has_event = Column(Boolean, default=False)
    event_name = Column(String(200), nullable=True)
    has_recommendation = Column(Boolean, default=False)
    recommended_price_yen = Column(Integer, nullable=True)
    has_decision = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<DailyCalendarStatus(date="'{self.date}', room_group="'{self.room_group}')>"
