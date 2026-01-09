import os
import pytest
import warnings

# Add dotenv for loading environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    warnings.warn("python-dotenv not installed. Cannot load .env file. Install with: pip install python-dotenv")

from makeimpact import (
    OneClickImpact, Environment
)
from makeimpact.exceptions import OneClickImpactError

# Get API key from environment variable (now loaded from .env if it exists)
API_KEY = os.environ.get("TEST_API_KEY")

# Skip all tests if no API key is provided
if not API_KEY:
    warnings.warn(
        "⚠️ No TEST_API_KEY environment variable found. Skipping live API tests.\n"
        "To run these tests, either:\n"
        "1. Create a .env file in the project root with: TEST_API_KEY=your_sandbox_api_key_here\n"
        "2. Set the environment variable: export TEST_API_KEY=your_sandbox_api_key_here"
    )


@pytest.fixture
def sdk():
    """Initialize SDK fixture"""
    if not API_KEY:
        pytest.skip("No TEST_API_KEY environment variable found")
    return OneClickImpact(API_KEY, Environment.SANDBOX)


class TestOneClickImpact:
    """Test cases for the OneClickImpact SDK"""

    class TestInitialization:
        """Tests for SDK initialization"""

        def test_empty_api_key(self):
            """Should throw error when API key is not provided"""
            with pytest.raises(ValueError) as excinfo:
                OneClickImpact("")
            assert "API key is required" in str(excinfo.value)

        def test_invalid_api_key(self):
            """Should throw error when API key does not exist"""
            invalid_sdk = OneClickImpact("incorrect_api_key", Environment.SANDBOX)
            with pytest.raises(OneClickImpactError) as excinfo:
                invalid_sdk.who_am_i()
            assert "API Key does not exist" in str(excinfo.value)

        def test_valid_api_key(self, sdk):
            """Should initialize with API key"""
            assert isinstance(sdk, OneClickImpact)

    class TestWhoAmI:
        """Tests for whoAmI method"""

        def test_verify_api_key(self, sdk):
            """Should verify API key"""
            response = sdk.who_am_i()
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "email")

    class TestGetImpact:
        """Tests for getImpact method"""

        def test_get_impact_statistics(self, sdk):
            """Should get impact statistics with user_impact and customer_impact breakdown"""
            response = sdk.get_impact()
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "tree_planted")
            assert hasattr(response, "waste_removed")
            assert hasattr(response, "carbon_captured")
            assert hasattr(response, "money_donated")
            
            # Check user_impact breakdown
            assert hasattr(response, "user_impact")
            assert hasattr(response.user_impact, "tree_planted")
            assert hasattr(response.user_impact, "waste_removed")
            assert hasattr(response.user_impact, "carbon_captured")
            assert hasattr(response.user_impact, "money_donated")
            
            # Check customer_impact breakdown
            assert hasattr(response, "customer_impact")
            assert hasattr(response.customer_impact, "tree_planted")
            assert hasattr(response.customer_impact, "waste_removed")
            assert hasattr(response.customer_impact, "carbon_captured")
            assert hasattr(response.customer_impact, "money_donated")

    class TestGetDailyImpact:
        """Tests for getDailyImpact method"""

        def test_get_daily_impact_no_filters(self, sdk):
            """Should get daily impact statistics without date filters"""
            response = sdk.get_daily_impact()
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "daily_impact")
            assert isinstance(response.daily_impact, list)
            
            # If there are any records, verify their structure
            if len(response.daily_impact) > 0:
                record = response.daily_impact[0]
                assert hasattr(record, "date")
                assert hasattr(record, "tree_planted")
                assert hasattr(record, "waste_removed")
                assert hasattr(record, "carbon_captured")
                assert hasattr(record, "money_donated")

        def test_get_daily_impact_with_date_range(self, sdk):
            """Should get daily impact statistics with date range filters"""
            response = sdk.get_daily_impact(
                start_date="2025-01-01",
                end_date="2025-12-31"
            )
            assert response is not None
            assert hasattr(response, "user_id")
            assert hasattr(response, "daily_impact")
            assert isinstance(response.daily_impact, list)

    class TestPlantTrees:
        """Tests for plantTree method"""

        def test_plant_trees(self, sdk):
            """Should plant trees"""
            response = sdk.plant_tree(amount=1)
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is None
            assert response.category is None

        def test_plant_trees_with_category(self, sdk):
            """Should plant trees with category"""
            response = sdk.plant_tree(amount=1, category="food")
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is None
            assert response.category == "food"

        def test_plant_trees_with_customer_info(self, sdk):
            """Should plant trees with customer info"""
            response = sdk.plant_tree(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            )
            assert response is not None
            assert response.user_id
            assert response.tree_planted == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"
            assert response.category is None

    class TestCleanOcean:
        """Tests for cleanOcean method"""

        def test_clean_ocean_waste(self, sdk):
            """Should clean ocean waste"""
            response = sdk.clean_ocean(amount=1)
            assert response is not None
            assert response.user_id
            assert response.waste_removed == 1
            assert response.time_utc
            assert response.customer is None

        def test_clean_ocean_waste_with_customer_info(self, sdk):
            """Should clean ocean waste with customer info"""
            response = sdk.clean_ocean(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            )
            assert response is not None
            assert response.user_id
            assert response.waste_removed == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestCaptureCarbon:
        """Tests for captureCarbon method"""

        def test_capture_carbon(self, sdk):
            """Should capture carbon"""
            response = sdk.capture_carbon(amount=1)
            assert response is not None
            assert response.user_id
            assert response.carbon_captured == 1
            assert response.time_utc
            assert response.customer is None

        def test_capture_carbon_with_customer_info(self, sdk):
            """Should capture carbon with customer info"""
            response = sdk.capture_carbon(
                amount=1,
                customer_email="test@example.com",
                customer_name="Test User"
            )
            assert response is not None
            assert response.user_id
            assert response.carbon_captured == 1
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestDonateMoney:
        """Tests for donateMoney method"""

        def test_donate_money(self, sdk):
            """Should donate money"""
            response = sdk.donate_money(amount=100)  # $1.00
            assert response is not None
            assert response.user_id
            assert response.money_donated == 100
            assert response.time_utc
            assert response.customer is None

        def test_donate_money_with_customer_info(self, sdk):
            """Should donate money with customer info"""
            response = sdk.donate_money(
                amount=100,  # $1.00
                customer_email="test@example.com",
                customer_name="Test User"
            )
            assert response is not None
            assert response.user_id
            assert response.money_donated == 100
            assert response.time_utc
            assert response.customer is not None
            assert response.customer.customer_id
            assert response.customer.customer_info is not None
            assert response.customer.customer_info.customer_email == "test@example.com"
            assert response.customer.customer_info.customer_name == "Test User"

    class TestGetRecords:
        """Tests for getRecords method"""

        def test_get_all_records(self, sdk):
            """Should get all records"""
            response = sdk.get_records()
            assert response is not None
            assert hasattr(response, "user_records")
            assert isinstance(response.user_records, list)

        def test_get_records_with_filters(self, sdk):
            """Should get records with filters"""
            response = sdk.get_records(
                filter_by="tree_planted",
                limit=5
            )
            assert response is not None
            assert hasattr(response, "user_records")
            assert isinstance(response.user_records, list)
            assert len(response.user_records) <= 5

        def test_get_records_with_pagination(self, sdk):
            """Should get records with pagination"""
            # Get first page with just one record
            first_page = sdk.get_records(limit=1)
            assert first_page is not None
            assert hasattr(first_page, "user_records")
            assert isinstance(first_page.user_records, list)
            assert len(first_page.user_records) <= 1
            
            # Check if there are more records (cursor exists)
            if first_page.cursor:
                # Use the cursor to get the next page
                second_page = sdk.get_records(
                    limit=1,
                    cursor=first_page.cursor
                )
                assert second_page is not None
                assert hasattr(second_page, "user_records")
                assert isinstance(second_page.user_records, list)
                
                # If we have records in both pages, they should be different
                if first_page.user_records and second_page.user_records:
                    # Check if records are different by comparing time_utc
                    assert first_page.user_records[0].time_utc != second_page.user_records[0].time_utc

    class TestGetCustomerRecords:
        """Tests for getCustomerRecords method"""

        def test_get_customer_records(self, sdk):
            """Should get customer records"""
            # First create a record with a customer
            sdk.plant_tree(
                amount=1,
                customer_email="test_customer@example.com",
                customer_name="Test Customer"
            )

            response = sdk.get_customer_records(
                customer_email="test_customer@example.com"
            )
            assert response is not None
            assert hasattr(response, "customer_records")
            assert isinstance(response.customer_records, list)

    class TestGetCustomers:
        """Tests for getCustomers method"""

        def test_get_all_customers(self, sdk):
            """Should get all customers"""
            response = sdk.get_customers()
            assert response is not None
            assert hasattr(response, "customers")
            assert isinstance(response.customers, list)

        def test_get_customer_by_email(self, sdk):
            """Should get customer by email"""
            # Create a customer first
            sdk.plant_tree(
                amount=1,
                customer_email="filtered_customer@example.com",
                customer_name="Filtered Customer"
            )

            response = sdk.get_customers(
                customer_email="filtered_customer@example.com"
            )
            assert response is not None
            assert hasattr(response, "customers")
            assert isinstance(response.customers, list)
            
            if response.customers:
                customer = response.customers[0]
                assert customer.customer_email == "filtered_customer@example.com"
                assert customer.customer_name == "Filtered Customer"
                assert customer.customer_id
                assert customer.onboarded_on
    
    class TestTrackImpact:
        """Tests for track method"""

        def test_track_tree_planting_impact(self, sdk):
            """Should track a tree planting impact record"""
            # First create an impact to track
            plant_response = sdk.plant_tree(amount=1)
            
            # Then track it
            track_response = sdk.track(
                user_id=plant_response.user_id,
                time_utc=plant_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            assert track_response.impact_initiated
            
            # Check that the specific impact type has the correct value
            if track_response.tree_planted is not None:
                assert track_response.tree_planted == 1
            
            # Verify optional fields are accessible (certificate only in production)
            # In sandbox, these fields should be None or not present
            assert hasattr(track_response, "certificate")
            assert hasattr(track_response, "impact_video")
            assert hasattr(track_response, "live_session_date")
            assert hasattr(track_response, "assigned_agent")
            assert hasattr(track_response, "project_location")
            assert hasattr(track_response, "location_map")

        def test_track_ocean_cleanup_impact(self, sdk):
            """Should track ocean cleanup impact"""
            # Create an ocean cleanup impact
            clean_response = sdk.clean_ocean(amount=5)
            
            # Track it
            track_response = sdk.track(
                user_id=clean_response.user_id,
                time_utc=clean_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            
            if track_response.waste_removed is not None:
                assert track_response.waste_removed == 5

        def test_track_carbon_capture_impact(self, sdk):
            """Should track carbon capture impact"""
            # Create a carbon capture impact
            carbon_response = sdk.capture_carbon(amount=10)
            
            # Track it
            track_response = sdk.track(
                user_id=carbon_response.user_id,
                time_utc=carbon_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            
            if track_response.carbon_captured is not None:
                assert track_response.carbon_captured == 10

        def test_track_money_donation_impact(self, sdk):
            """Should track money donation impact"""
            # Create a money donation impact
            donate_response = sdk.donate_money(amount=100)
            
            # Track it
            track_response = sdk.track(
                user_id=donate_response.user_id,
                time_utc=donate_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            
            if track_response.money_donated is not None:
                assert track_response.money_donated == 100

        def test_track_impact_with_category(self, sdk):
            """Should track impact with food category"""
            # Create an impact with food category
            plant_response = sdk.plant_tree(amount=1, category="food")
            
            # Track it
            track_response = sdk.track(
                user_id=plant_response.user_id,
                time_utc=plant_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            assert track_response.category == "food"

        def test_track_optional_fields(self, sdk):
            """Should include optional tracking fields when available"""
            # Create an impact
            plant_response = sdk.plant_tree(amount=1)
            
            # Track it
            track_response = sdk.track(
                user_id=plant_response.user_id,
                time_utc=plant_response.time_utc
            )
            
            assert track_response is not None
            assert track_response.tracking_id
            
            # These fields may or may not be present depending on impact status
            # Just verify they're either None or have the correct type
            if track_response.donation_available:
                assert isinstance(track_response.donation_available, str)
            if track_response.assigned_agent:
                assert isinstance(track_response.assigned_agent, str)
            if track_response.impact_completed:
                assert isinstance(track_response.impact_completed, str)
            if track_response.is_test_transaction is not None:
                assert isinstance(track_response.is_test_transaction, bool)
