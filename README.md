# 🌱 MakeImpact Python SDK

[![PyPI version](https://img.shields.io/pypi/v/makeimpact.svg)](https://pypi.org/project/makeimpact/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)

> Official Python SDK for 1ClickImpact - Easily integrate impact actions into your Python applications

## 📦 Installation

```bash
pip install makeimpact
# or
poetry add makeimpact
```

## 🚀 Getting Started

You'll need an API key to use this SDK. You can get your API key from the [1ClickImpact Account API Keys page](https://1clickimpact.com/account/api-keys).

```python
from makeimpact import OneClickImpact, Environment

# Initialize the SDK with your API key (production environment by default)
sdk = OneClickImpact("your_api_key")

# Create environmental impact with just a few lines of code
sdk.plant_tree(amount=1)
sdk.clean_ocean(amount=5)
sdk.capture_carbon(amount=2)
```

## 🌍 Environmental Impact Actions

### 🌳 Plant Trees

Help combat deforestation and climate change by planting trees.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Plant a single tree
sdk.plant_tree(amount=1)

# Plant trees with a specific category
sdk.plant_tree(amount=10, category="food")

# Plant trees with customer tracking
sdk.plant_tree(
    amount=5,
    customer_email="customer@example.com",
    customer_name="John Doe"
)
```

### 🌊 Clean Ocean Plastic

Remove plastic waste from our oceans to protect marine life.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Clean 5 pounds of ocean plastic
sdk.clean_ocean(amount=5)

# Clean ocean plastic with customer tracking
sdk.clean_ocean(
    amount=10,
    customer_email="customer@example.com",
    customer_name="John Doe"
)
```

### ♻️ Capture Carbon

Reduce greenhouse gas emissions by capturing carbon.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Capture 2 pounds of carbon
sdk.capture_carbon(amount=2)

# Capture carbon with customer tracking
sdk.capture_carbon(
    amount=5,
    customer_email="customer@example.com",
    customer_name="John Doe"
)
```

### 💰 Donate Money

Support any cause through direct monetary donations.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Donate $1.00 (amount in cents)
sdk.donate_money(amount=100)

# Donate with customer tracking
sdk.donate_money(
    amount=500,  # $5.00
    customer_email="customer@example.com",
    customer_name="John Doe"
)
```

> **Note**: To set up a custom cause for donations, please contact 1ClickImpact directly.
> All causes must be vetted and approved to ensure they meet their standards for transparency and impact.

## 📊 Data Access & Reporting

### Get Records

Retrieve impact records with optional filtering.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Get all records
records = sdk.get_records()

# Filter records by type
tree_records = sdk.get_records(filter_by="tree_planted")

# Filter records by date range
recent_records = sdk.get_records(
    start_date="2023-01-01",
    end_date="2023-12-31"
)

# Pagination
paginated_records = sdk.get_records(
    cursor="cursor_from_previous_response",
    limit=10
)
```

### Get Customer Records

Retrieve records for specific customers.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Get records for a specific customer
customer_records = sdk.get_customer_records(
    customer_email="customer@example.com"
)

# Filter customer records by type
customer_tree_records = sdk.get_customer_records(
    customer_email="customer@example.com",
    filter_by="tree_planted"
)
```

### Get Customers

Retrieve customer information.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Get all customers (default limit is 10)
customers = sdk.get_customers()

# Get customers with filtering and pagination
filtered_customers = sdk.get_customers(
    customer_email="example@email.com",  # Optional: Filter by email
    limit=50,  # Optional: Limit results (1-1000)
    cursor="cursor_from_previous_response"  # Optional: For pagination
)
```

### Get Impact

Get aggregated impact statistics.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Get overall impact statistics for your organization
impact = sdk.get_impact()

print(f"Trees planted: {impact.tree_planted}")
print(f"Ocean waste removed: {impact.waste_removed} lbs")
print(f"Carbon captured: {impact.carbon_captured} lbs")
print(f"Money donated: ${impact.money_donated / 100}")
```

### Who Am I

Verify your API key and get account information.

```python
from makeimpact import OneClickImpact

sdk = OneClickImpact("your_api_key")

# Verify API key and get account information
account_info = sdk.who_am_i()
```

## ⚙️ Configuration

### Environments

The SDK supports two environments:

- **Production** (default): Uses the live API at `https://api.1clickimpact.com`
- **Sandbox**: Uses the testing API at `https://sandbox.1clickimpact.com`

To use the sandbox environment for testing:

```python
from makeimpact import OneClickImpact, Environment

# Initialize with sandbox environment
sdk = OneClickImpact("your_test_api_key", Environment.SANDBOX)
```

## 🔗 Additional Resources

- [1ClickImpact API Documentation](https://docs.1clickimpact.com/plant-trees)
- [1ClickImpact Website](https://www.1clickimpact.com)
- [Pricing & API Keys](https://www.1clickimpact.com/pricing)

## 📄 License

MIT
