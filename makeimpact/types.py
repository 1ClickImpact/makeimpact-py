from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Union, Dict, Any


class Environment(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


@dataclass
class CustomerInfo:
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None


@dataclass
class Customer:
    customer_id: str
    customer_info: CustomerInfo


@dataclass
class PlantTreeParams:
    amount: int
    category: Optional[str] = None
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    notify: Optional[bool] = None


@dataclass
class PlantTreeResponse:
    user_id: str
    tree_planted: int
    time_utc: str  # Moved before optional fields
    category: Optional[str] = None
    customer: Optional[Customer] = None


@dataclass
class CleanOceanParams:
    amount: int
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    notify: Optional[bool] = None


@dataclass
class CleanOceanResponse:
    user_id: str
    waste_removed: int
    time_utc: str  # Moved before optional fields
    customer: Optional[Customer] = None


@dataclass
class CaptureCarbonParams:
    amount: int
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    notify: Optional[bool] = None


@dataclass
class CaptureCarbonResponse:
    user_id: str
    carbon_captured: int
    time_utc: str  # Moved before optional fields
    customer: Optional[Customer] = None


@dataclass
class DonateMoneyParams:
    amount: int
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    notify: Optional[bool] = None


@dataclass
class DonateMoneyResponse:
    user_id: str
    money_donated: int
    time_utc: str  # Moved before optional fields
    customer: Optional[Customer] = None


@dataclass
class ErrorResponse:
    type: str
    message: str


@dataclass
class GetRecordsParams:
    filter_by: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    cursor: Optional[str] = None
    limit: Optional[int] = None


@dataclass
class BaseRecord:
    user_id: str
    time_utc: str


@dataclass
class TreePlantedRecord(BaseRecord):
    tree_planted: int
    category: Optional[str] = None


@dataclass
class WasteRemovedRecord(BaseRecord):
    waste_removed: int


@dataclass
class CarbonCapturedRecord(BaseRecord):
    carbon_captured: int


@dataclass
class MoneyDonatedRecord(BaseRecord):
    money_donated: int


ImpactRecord = Union[TreePlantedRecord, WasteRemovedRecord, CarbonCapturedRecord, MoneyDonatedRecord]


@dataclass
class GetRecordsResponse:
    user_records: List[ImpactRecord]
    cursor: Optional[str] = None


@dataclass
class GetCustomerRecordsParams(GetRecordsParams):
    customer_email: Optional[str] = None


@dataclass
class GetCustomersParams:
    customer_email: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


@dataclass
class CustomerDetails:
    customer_id: str
    customer_email: str
    onboarded_on: str  # Moved before the optional field
    customer_name: Optional[str] = None


@dataclass
class GetCustomersResponse:
    customers: List[CustomerDetails]
    cursor: Optional[str] = None


@dataclass
class ImpactResponse:
    user_id: str
    tree_planted: int
    waste_removed: int
    carbon_captured: int
    money_donated: int


@dataclass
class WhoAmIResponse:
    user_id: str
    email: str


@dataclass
class BaseRecordWithCustomer(BaseRecord):
    customer: Customer  # If this doesn't have a default, it must come before any fields with defaults


@dataclass
class TreePlantedRecordWithCustomer(BaseRecordWithCustomer):
    tree_planted: int
    category: Optional[str] = None


@dataclass
class WasteRemovedRecordWithCustomer(BaseRecordWithCustomer):
    waste_removed: int


@dataclass
class CarbonCapturedRecordWithCustomer(BaseRecordWithCustomer):
    carbon_captured: int


@dataclass
class MoneyDonatedRecordWithCustomer(BaseRecordWithCustomer):
    money_donated: int


CustomerImpactRecord = Union[
    TreePlantedRecordWithCustomer,
    WasteRemovedRecordWithCustomer,
    CarbonCapturedRecordWithCustomer,
    MoneyDonatedRecordWithCustomer
]


@dataclass
class GetCustomerRecordsResponse:
    customer_records: List[CustomerImpactRecord]
    cursor: Optional[str] = None

@dataclass
class TrackParams:
    user_id: str
    time_utc: str


@dataclass
class TrackResponse:
    tracking_id: str
    impact_initiated: str
    tree_planted: Optional[int] = None
    waste_removed: Optional[int] = None
    carbon_captured: Optional[int] = None
    money_donated: Optional[int] = None
    category: Optional[str] = None
    donation_available: Optional[str] = None
    donation_sent: Optional[str] = None
    assigned_agent: Optional[str] = None
    project_location: Optional[str] = None
    location_map: Optional[str] = None
    impact_completed: Optional[str] = None
    donation_category: Optional[str] = None
    impact_video: Optional[str] = None
    live_session_date: Optional[str] = None
    is_test_transaction: Optional[bool] = None
    is_bonus_impact: Optional[bool] = None