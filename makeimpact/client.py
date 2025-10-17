from typing import Dict, Any, Optional, List
import requests

from .types import (
    Environment,
    PlantTreeResponse,
    CleanOceanResponse,
    CaptureCarbonResponse,
    DonateMoneyResponse,
    GetRecordsResponse,
    GetCustomerRecordsResponse,
    GetCustomersResponse,
    ImpactResponse,
    WhoAmIResponse,
    TrackResponse,
    Customer,
    CustomerInfo,
    CustomerDetails,
    TreePlantedRecord,
    WasteRemovedRecord,
    CarbonCapturedRecord,
    MoneyDonatedRecord,
    TreePlantedRecordWithCustomer,
    WasteRemovedRecordWithCustomer,
    CarbonCapturedRecordWithCustomer,
    MoneyDonatedRecordWithCustomer
)
from .exceptions import OneClickImpactError


class OneClickImpact:
    """
    Client for interacting with the 1ClickImpact API
    """

    def __init__(self, api_key: str, environment: Environment = Environment.PRODUCTION):
        """
        Initialize the 1ClickImpact SDK
        
        Args:
            api_key: Your 1ClickImpact API key (get a free key from https://www.1clickimpact.com/pricing)
            environment: Optional: Specify whether to use production or sandbox environment
        """
        if not api_key:
            raise ValueError("API key is required to initialize the 1ClickImpact SDK")
        
        self.api_key = api_key
        
        # Set the base URL based on the environment
        self.base_url = (
            "https://sandbox.1clickimpact.com" 
            if environment == Environment.SANDBOX 
            else "https://api.1clickimpact.com"
        )

    def plant_tree(self, 
                  amount: int, 
                  category: Optional[str] = None, 
                  customer_email: Optional[str] = None, 
                  customer_name: Optional[str] = None,
                  notify: Optional[bool] = None) -> PlantTreeResponse:
        """
        Plant trees through 1ClickImpact
        
        Args:
            amount: Number of trees to plant (1-10,000,000)
            category: Optional: Category for the tree planting
            customer_email: Optional: Customer's email
            customer_name: Optional: Customer's name (only used if email is provided)
            notify: Optional: If set to true, the customer will receive an email confirmation for this impact. Defaults to true. Note: notifications are always disabled in the sandbox environment.
                
        Returns:
            PlantTreeResponse: Response containing details about the planted trees
        """
        body = {"amount": amount}
        
        if category:
            body["category"] = category
        if customer_email:
            body["customer_email"] = customer_email
            if customer_name:
                body["customer_name"] = customer_name
        if notify is not None:
            body["notify"] = notify
                
        response = self._make_request("/v1/plant_tree", body)
        
        # Transform API response to match the PlantTreeResponse interface
        return PlantTreeResponse(
            user_id=response["user_id"],
            tree_planted=response["tree_planted"],
            category=response.get("category"),
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def clean_ocean(self,
                   amount: int,
                   customer_email: Optional[str] = None,
                   customer_name: Optional[str] = None,
                   notify: Optional[bool] = None) -> CleanOceanResponse:
        """
        Clean ocean plastic through 1ClickImpact
        
        Args:
            amount: Amount of waste to clean in pounds (lbs) (1-10,000,000)
            customer_email: Optional: Customer's email
            customer_name: Optional: Customer's name (only used if email is provided)
            notify: Optional: If set to true, the customer will receive an email confirmation for this impact. Defaults to true. Note: notifications are always disabled in the sandbox environment.
                
        Returns:
            CleanOceanResponse: Response containing details about the waste removed
        """
        body = {"amount": amount}
        
        if customer_email:
            body["customer_email"] = customer_email
            if customer_name:
                body["customer_name"] = customer_name
        if notify is not None:
            body["notify"] = notify
                
        response = self._make_request("/v1/clean_ocean", body)
        
        # Transform API response to match the CleanOceanResponse interface
        return CleanOceanResponse(
            user_id=response["user_id"],
            waste_removed=response["waste_removed"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def capture_carbon(self,
                      amount: int,
                      customer_email: Optional[str] = None,
                      customer_name: Optional[str] = None,
                      notify: Optional[bool] = None) -> CaptureCarbonResponse:
        """
        Capture carbon through 1ClickImpact
        
        Args:
            amount: Amount of carbon to capture in pounds (lbs) (1-10,000,000)
            customer_email: Optional: Customer's email
            customer_name: Optional: Customer's name (only used if email is provided)
            notify: Optional: If set to true, the customer will receive an email confirmation for this impact. Defaults to true. Note: notifications are always disabled in the sandbox environment.
                
        Returns:
            CaptureCarbonResponse: Response containing details about the carbon captured
        """
        body = {"amount": amount}
        
        if customer_email:
            body["customer_email"] = customer_email
            if customer_name:
                body["customer_name"] = customer_name
        if notify is not None:
            body["notify"] = notify
                
        response = self._make_request("/v1/capture_carbon", body)
        
        # Transform API response to match the CaptureCarbonResponse interface
        return CaptureCarbonResponse(
            user_id=response["user_id"],
            carbon_captured=response["carbon_captured"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def donate_money(self,
                    amount: int,
                    customer_email: Optional[str] = None,
                    customer_name: Optional[str] = None,
                    notify: Optional[bool] = None) -> DonateMoneyResponse:
        """
        Donate money through 1ClickImpact
        
        Args:
            amount: Amount in smallest USD units (cents). For example, $1 = 100, $0.10 = 10 (1-1,000,000,000)
            customer_email: Optional: Customer's email
            customer_name: Optional: Customer's name (only used if email is provided)
            notify: Optional: If set to true, the customer will receive an email confirmation for this impact. Defaults to true. Note: notifications are always disabled in the sandbox environment.

        Returns:
            DonateMoneyResponse: Response containing details about the money donated
        """
        body = {"amount": amount}
        
        if customer_email:
            body["customer_email"] = customer_email
            if customer_name:
                body["customer_name"] = customer_name
        if notify is not None:
            body["notify"] = notify
                
        response = self._make_request("/v1/donate_money", body)
        
        # Transform API response to match the DonateMoneyResponse interface
        return DonateMoneyResponse(
            user_id=response["user_id"],
            money_donated=response["money_donated"],
            customer=self._transform_customer(response.get("customer")),
            time_utc=response["time_utc"],
        )

    def get_impact(self) -> ImpactResponse:
        """
        Get impact statistics
        
        Returns:
            ImpactResponse: Impact statistics for your organization
        """
        response = self._make_request("/v1/impact", None, "GET")
        
        return ImpactResponse(
            user_id=response["user_id"],
            tree_planted=response.get("tree_planted", 0),
            waste_removed=response.get("waste_removed", 0),
            carbon_captured=response.get("carbon_captured", 0),
            money_donated=response.get("money_donated", 0),
        )

    def who_am_i(self) -> WhoAmIResponse:
        """
        Verify API key and get account information
        
        Returns:
            WhoAmIResponse: Account information for the provided API key
        """
        response = self._make_request("/v1/whoami", None, "GET")
        
        return WhoAmIResponse(
            user_id=response["user_id"],
            email=response["email"],
        )

    def get_records(self,
                   filter_by: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   cursor: Optional[str] = None,
                   limit: Optional[int] = None) -> GetRecordsResponse:
        """
        Get impact records
        
        Args:
            filter_by: Optional: Filter records by type. The value could be either 
                      "tree_planted", "waste_removed", "carbon_captured", or "money_donated".
            start_date: Optional: Filter records created on or after this date (format: YYYY-MM-DD)
            end_date: Optional: Filter records created on or before this date (format: YYYY-MM-DD)
            cursor: Optional: Pagination cursor from previous response for fetching next page
            limit: Optional: Maximum number of records to return (1-1000, default: 10)
                
        Returns:
            GetRecordsResponse: Records based on the provided filters
        """
        query_params = {}
        if filter_by:
            query_params["filter_by"] = filter_by
        if start_date:
            query_params["start_date"] = start_date
        if end_date:
            query_params["end_date"] = end_date
        if cursor:
            query_params["cursor"] = cursor
        if limit is not None:
            query_params["limit"] = limit
            
        endpoint = "/v1/records"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response format to match our SDK interface
        user_records = []
        for record in response["user_records"]:
            base_record = {
                "user_id": record["user_id"],
                "time_utc": record["time_utc"],
            }
            
            if "tree_planted" in record:
                user_records.append(TreePlantedRecord(
                    **base_record,
                    tree_planted=record["tree_planted"],
                    category=record.get("category")
                ))
            elif "waste_removed" in record:
                user_records.append(WasteRemovedRecord(
                    **base_record,
                    waste_removed=record["waste_removed"]
                ))
            elif "carbon_captured" in record:
                user_records.append(CarbonCapturedRecord(
                    **base_record,
                    carbon_captured=record["carbon_captured"]
                ))
            elif "money_donated" in record:
                user_records.append(MoneyDonatedRecord(
                    **base_record,
                    money_donated=record["money_donated"]
                ))
                
        return GetRecordsResponse(
            user_records=user_records,
            cursor=response.get("cursor"),
        )

    def get_customer_records(self,
                            customer_email: Optional[str] = None,
                            filter_by: Optional[str] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            cursor: Optional[str] = None,
                            limit: Optional[int] = None) -> GetCustomerRecordsResponse:
        """
        Get customer records
        
        Args:
            customer_email: Optional: Filter records by customer email
            filter_by: Optional: Filter records by type. The value could be either 
                      "tree_planted", "waste_removed", "carbon_captured", or "money_donated".
            start_date: Optional: Filter records created on or after this date (format: YYYY-MM-DD)
            end_date: Optional: Filter records created on or before this date (format: YYYY-MM-DD)
            cursor: Optional: Pagination cursor from previous response for fetching next page
            limit: Optional: Maximum number of records to return (1-1000, default: 10)
                
        Returns:
            GetCustomerRecordsResponse: Customer records based on the provided filters
        """
        query_params = {}
        if customer_email:
            query_params["customer_email"] = customer_email
        if filter_by:
            query_params["filter_by"] = filter_by
        if start_date:
            query_params["start_date"] = start_date
        if end_date:
            query_params["end_date"] = end_date
        if cursor:
            query_params["cursor"] = cursor
        if limit is not None:
            query_params["limit"] = limit
            
        endpoint = "/v1/customer_records"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response format to match our SDK interface
        customer_records = []
        for record in response["customer_records"]:
            base_record = {
                "user_id": record["user_id"],
                "time_utc": record["time_utc"],
                "customer": self._transform_customer(record["customer"]),
            }
            
            if "tree_planted" in record:
                customer_records.append(TreePlantedRecordWithCustomer(
                    **base_record,
                    tree_planted=record["tree_planted"],
                    category=record.get("category")
                ))
            elif "waste_removed" in record:
                customer_records.append(WasteRemovedRecordWithCustomer(
                    **base_record,
                    waste_removed=record["waste_removed"]
                ))
            elif "carbon_captured" in record:
                customer_records.append(CarbonCapturedRecordWithCustomer(
                    **base_record,
                    carbon_captured=record["carbon_captured"]
                ))
            elif "money_donated" in record:
                customer_records.append(MoneyDonatedRecordWithCustomer(
                    **base_record,
                    money_donated=record["money_donated"]
                ))
                
        return GetCustomerRecordsResponse(
            customer_records=customer_records,
            cursor=response.get("cursor"),
        )

    def get_customers(self,
                     customer_email: Optional[str] = None,
                     limit: Optional[int] = None,
                     cursor: Optional[str] = None) -> GetCustomersResponse:
        """
        Get customers
        
        Args:
            customer_email: Optional: Filter customers by email
            limit: Optional: Maximum number of customers to return (1-1000, default: 10)
            cursor: Optional: Pagination cursor from previous response for fetching next page
                
        Returns:
            GetCustomersResponse: Customers based on the provided filters
        """
        query_params = {}
        if customer_email:
            query_params["customer_email"] = customer_email
        if limit is not None:
            query_params["limit"] = limit
        if cursor:
            query_params["cursor"] = cursor
            
        endpoint = "/v1/customers"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform the API response to match our SDK interface
        customers = []
        for customer in response["customers"]:
            customers.append(CustomerDetails(
                customer_id=customer["customer_id"],
                customer_email=customer["customer_email"],
                customer_name=customer.get("customer_name"),
                onboarded_on=customer["onboarded_on"],
            ))
                
        return GetCustomersResponse(
            customers=customers,
            cursor=response.get("cursor"),
        )
    
    def track(self,
             user_id: str,
             time_utc: str) -> TrackResponse:
        """
        Track the complete lifecycle and current status of a specific impact
        
        Args:
            user_id: The user ID from the impact record you want to track (format: "U1234"). 
                    Obtain this from the user_id field returned by get_records() or get_customer_records().
            time_utc: The UTC timestamp when the impact was made (ISO 8601 format: "YYYY-MM-DDTHH:mm:ss.sssZ"). 
                     Obtain this from the time_utc field in the same record as the user_id.
                
        Returns:
            TrackResponse: Detailed tracking information about the impact including project location,
                          assigned agents, completion status, and documentation
        """
        query_params = {
            "user_id": user_id,
            "time_utc": time_utc
        }
        
        endpoint = "/v1/track"
        response = self._make_request(endpoint, None, "GET", query_params)
        
        # Transform API response to match the TrackResponse interface
        return TrackResponse(
            tracking_id=response["tracking_id"],
            impact_initiated=response["impact_initiated"],
            tree_planted=response.get("tree_planted"),
            waste_removed=response.get("waste_removed"),
            carbon_captured=response.get("carbon_captured"),
            money_donated=response.get("money_donated"),
            category=response.get("category"),
            donation_available=response.get("donation_available"),
            donation_sent=response.get("donation_sent"),
            assigned_agent=response.get("assigned_agent"),
            project_location=response.get("project_location"),
            location_map=response.get("location_map"),
            impact_completed=response.get("impact_completed"),
            donation_category=response.get("donation_category"),
            impact_video=response.get("impact_video"),
            live_session_date=response.get("live_session_date"),
            is_test_transaction=response.get("is_test_transaction"),
            is_bonus_impact=response.get("is_bonus_impact"),
        )

    def _make_request(
        self, 
        endpoint: str, 
        body: Optional[Dict[str, Any]] = None, 
        method: str = "POST",
        query_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Makes a request to the 1ClickImpact API
        
        Args:
            endpoint: API endpoint
            body: Request body
            method: HTTP method (default: POST)
            query_params: Query parameters to include in the URL
            
        Returns:
            API response
            
        Raises:
            OneClickImpactError: If the API returns an error
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            }
            
            url = f"{self.base_url}{endpoint}"
            
            if query_params:
                # Add query parameters to URL
                query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
                url = f"{url}?{query_string}"
            
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body if body else {})
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_data = response.json()
            
            if not response.ok:
                if "type" in response_data and "message" in response_data:
                    raise OneClickImpactError(
                        message=response_data["message"],
                        error_type=response_data["type"]
                    )
                raise OneClickImpactError(f"Request failed with status {response.status_code}")
            
            return response_data
        
        except requests.RequestException as e:
            raise OneClickImpactError(f"1ClickImpact API Error: {str(e)}")
        except Exception as e:
            raise OneClickImpactError(f"1ClickImpact SDK Error: {str(e)}")

    def _transform_customer(self, customer_data: Optional[Dict[str, Any]]) -> Optional[Customer]:
        """
        Helper function to transform customer data from API format to SDK format
        
        Args:
            customer_data: Customer data from the API
            
        Returns:
            Transformed Customer object or None if customer_data is None
        """
        if not customer_data:
            return None
            
        return Customer(
            customer_id=customer_data["customer_id"],
            customer_info=CustomerInfo(
                customer_email=customer_data.get("customer_email"),
                customer_name=customer_data.get("customer_name"),
            )
        )
