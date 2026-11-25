"""
Pydantic schemas for API request/response validation.
Week 2: API contract for Member 4 and Member 7 integration.
Defines data structures for hotels, competitor prices, events, and import history.
"""
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# =============================================================================
# ENUMS (Shared across schemas)
# =============================================================================

class DataKind(str, Enum):
    """Classification of data source for median calculations."""
    PUBLIC = "PUBLIC"
    SAMPLE = "SAMPLE"
    PROVIDED = "PROVIDED"
    DERIVED = "DERIVED"


class SalesStatus(str, Enum):
    """Hotel room sales status."""
    ON_SALE = "ON_SALE"
    STOPPED = "STOPPED"
    UN_SOLD = "UN_SOLD"


class RoomGroup(str, Enum):
    """Room category grouping."""
    SINGLE_SMOKING = "SINGLE_SMOKING"
    SINGLE_NON_SMOKING = "SINGLE_NON_SMOKING"
    TWIN_SMOKING = "TWIN_SMOKING"
    TWIN_NON_SMOKING = "TWIN_NON_SMOKING"
    DOUBLE_SMOKING = "DOUBLE_SMOKING"
    DOUBLE_NON_SMOKING = "DOUBLE_NON_SMOKING"
    SUITE = "SUITE"


class MealPlan(str, Enum):
    """Meal plan options."""
    ROOM_ONLY = "ROOM_ONLY"
    BREAKFAST = "BREAKFAST"
    DINNER = "DINNER"
    BREAKFAST_DINNER = "BREAKFAST_DINNER"


class PriceSource(str, Enum):
    """Source of competitor price data."""
    OTA = "OTA"
    DIRECT = "DIRECT"
    MANUAL = "MANUAL"
    IMPORTED = "IMPORTED"


class EventType(str, Enum):
    """Type of local event affecting pricing."""
    FESTIVAL = "FESTIVAL"
    CONCERT = "CONCERT"
    CONVENTION = "CONVENTION"
    HOLIDAY = "HOLIDAY"
    WEATHER = "WEATHER"


class StaffDecision(str, Enum):
    """Staff decision on price recommendation."""
    ADOPT = "ADOPT"
    MODIFY = "MODIFY"
    SKIP = "SKIP"


class ImportStatus(str, Enum):
    """Status of CSV import operation."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class ComparisonRequest(BaseModel):
    stay_date: date = Field(..., description="Target stay date")
    room_group: RoomGroup = Field(..., description="Room category group")
    adults: int = Field(..., ge=1, le=10, description="Number of adults")
    nights: int = Field(..., ge=1, le=30, description="Number of nights")
    meal_plan: MealPlan = Field(..., description="Meal plan option")


class CalendarRequest(BaseModel):
    start_date: date = Field(..., description="Calendar start date")
    end_date: date = Field(..., description="Calendar end date (max 6 months)")
    room_group: Optional[RoomGroup] = Field(None, description="Filter by room group")


class RecommendationRequest(BaseModel):
    stay_date: date = Field(..., description="Target stay date")
    room_group: RoomGroup = Field(..., description="Room category group")
    adults: int = Field(..., ge=1, le=10, description="Number of adults")
    nights: int = Field(..., ge=1, le=30, description="Number of nights")
    meal_plan: MealPlan = Field(..., description="Meal plan option")


class DecisionRequest(BaseModel):
    proposal_id: str = Field(..., description="Unique proposal identifier")
    decision: StaffDecision = Field(..., description="Staff decision")
    modified_price: Optional[int] = Field(None, ge=0, description="Modified price if ADOPT or MODIFY")
    reason: Optional[str] = Field(None, max_length=500, description="Decision reason in Japanese")


class ImportRequest(BaseModel):
    filename: str = Field(..., description="Source filename")
    data_kind: DataKind = Field(..., description="Data classification")
    target_table: str = Field(..., description="Target table name")


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class HotelResponse(BaseModel):
    hotel_id: str = Field(..., description="Unique hotel identifier")
    hotel_name: str = Field(..., description="Hotel name in Japanese")
    sales_status: SalesStatus = Field(..., description="Current sales status")
    current_price_yen: Optional[int] = Field(None, ge=0, description="Current listed price")
    recommended_price_yen: Optional[int] = Field(None, ge=0, description="AI-recommended price")

    class Config:
        from_attributes = True


class CompetitorPriceResponse(BaseModel):
    hotel_id: str = Field(..., description="Competitor hotel ID")
    hotel_name: str = Field(..., description="Competitor hotel name")
    price_yen: Optional[int] = Field(None, ge=0, description="Competitor price (null if unavailable)")
    source_url: Optional[str] = Field(None, description="Source URL of price")
    source: PriceSource = Field(..., description="Data source type")
    collected_at: datetime = Field(..., description="Price collection timestamp")
    missing_reason: Optional[str] = Field(None, description="Reason if price is null")

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    event_name: str = Field(..., description="Event name")
    event_type: EventType = Field(..., description="Event category")
    event_date: date = Field(..., description="Event date")
    impact_level: int = Field(..., ge=1, le=5, description="Pricing impact level")
    description: Optional[str] = Field(None, description="Event description")

    class Config:
        from_attributes = True


class ImportHistoryResponse(BaseModel):
    import_id: str = Field(..., description="Unique import identifier")
    filename: str = Field(..., description="Source filename")
    target_table: str = Field(..., description="Target database table")
    data_kind: DataKind = Field(..., description="Data classification")
    row_count: int = Field(..., description="Number of rows imported")
    status: ImportStatus = Field(..., description="Import status")
    imported_at: datetime = Field(..., description="Import timestamp")
    error_row: Optional[int] = Field(None, description="Failed row number if failed")

    class Config:
        from_attributes = True


class ComparisonResponse(BaseModel):
    data_kind: DataKind = Field(..., description="Data classification")
    dataset_version: str = Field(..., description="Dataset version identifier")
    stay_date: date = Field(..., description="Target stay date")
    room_group: RoomGroup = Field(..., description="Room category group")
    adults: int = Field(..., description="Number of adults")
    nights: int = Field(..., description="Number of nights")
    meal_plan: MealPlan = Field(..., description="Meal plan option")
    own_hotel: HotelResponse = Field(..., description="Own hotel information")
    competitors: List[CompetitorPriceResponse] = Field(..., description="Competitor prices")
    median_yen: Optional[int] = Field(None, description="Median competitor price")
    source_count: int = Field(..., description="Number of price sources")
    collected_at: datetime = Field(..., description="Data collection timestamp")


class CalendarDayResponse(BaseModel):
    date: date = Field(..., description="Calendar date")
    room_group: RoomGroup = Field(..., description="Room category")
    sales_status: SalesStatus = Field(..., description="Sales status")
    current_price_yen: Optional[int] = Field(None, description="Current price")
    has_event: bool = Field(False, description="Event affecting this date")
    event_name: Optional[str] = Field(None, description="Event name if applicable")
    has_recommendation: bool = Field(False, description="Price recommendation available")
    recommended_price_yen: Optional[int] = Field(None, description="AI-recommended price")
    has_decision: bool = Field(False, description="Staff decision made")


class CalendarResponse(BaseModel):
    start_date: date = Field(..., description="Calendar start date")
    end_date: date = Field(..., description="Calendar end date")
    room_group: Optional[RoomGroup] = Field(None, description="Filtered room group")
    days: List[CalendarDayResponse] = Field(..., description="Daily statuses")


class RecommendationResponse(BaseModel):
    proposal_id: str = Field(..., description="Unique proposal identifier")
    stay_date: date = Field(..., description="Target stay date")
    room_group: RoomGroup = Field(..., description="Room category group")
    own_hotel: HotelResponse = Field(..., description="Own hotel current status")
    breakdown: dict = Field(..., description="Recommendation calculation breakdown")
    hold_reasons: List[str] = Field(default_factory=list, description="Reasons for price hold")
    rule_version: str = Field(..., description="Pricing rule version")
    valid_until: datetime = Field(..., description="Proposal expiration")
    data_kind: DataKind = Field(..., description="Data classification")


class DecisionResponse(BaseModel):
    decision_id: str = Field(..., description="Unique decision identifier")
    proposal_id: str = Field(..., description="Related proposal identifier")
    decision: StaffDecision = Field(..., description="Staff decision made")
    final_price_yen: int = Field(..., description="Final decided price")
    decided_by: str = Field(..., description="Staff identifier")
    reason: Optional[str] = Field(None, description="Decision reason")
    decided_at: datetime = Field(..., description="Decision timestamp")


class ImportResponse(BaseModel):
    import_id: str = Field(..., description="Unique import identifier")
    status: ImportStatus = Field(..., description="Import status")
    row_count: int = Field(..., description="Rows processed")
    duration_ms: int = Field(..., description="Import duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error details if failed")
    error_row: Optional[int] = Field(None, description="Failed row number")
    dataset_version: str = Field(..., description="New dataset version")


class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Health status")
    member: str = Field(..., description="Backend member identifier")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database connection status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)