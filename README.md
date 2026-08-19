# Illumi
Illumi is an intelligent, judgment-free personal financial management (PFM) mobile chat assistant designed to provide users with conversational, 
natural-language insights into their historical spending data. Built with a modern Python ecosystem and a mobile banking user experience, 
Illumi transforms raw financial statements into actionable insights.


## Requirements
needs a .env file in the root folder with an AI api key to run



## data
For each transaction in the personal statement it has beeen enriched in the following ways:

1. Extract and normalize the merchant name.
   - Remove terminal IDs, store numbers, dates, transaction references, location suffixes, card numbers, and payment processor noise.
   - Convert merchant names to a canonical consumer-facing brand name.
   - Examples:
     "SQ *JOES COFFEE LONDON" -> "Joe's Coffee"
     "TESCO STORES 5432 SPALDING" -> "Tesco"
     "AMZN MKTPLACE PMTS" -> "Amazon"
     "UBER *TRIP HELP.UBER.COM" -> "Uber"

2. Assign a spending category from this list:
   - Dining
   - Groceries
   - Transport
   - Fuel
   - Shopping
   - Entertainment
   - Travel
   - Utilities
   - Healthcare
   - Insurance
   - Education
   - Subscriptions
   - Financial Services
   - Government
   - Housing
   - Income
   - Transfer
   - Cash Withdrawal
   - Uncategorized

3. Return a confidence score between 0 and 1.

4. If the merchant cannot be reliably identified:
   - keep the best cleaned version
   - assign "Uncategorized"
   - lower confidence


For each transaction the following sub fields wre added:

1. subcategory
   * More granular classification within the category.
   * Examples:
      * Dining → Fast Food, Restaurant, Coffee Shop
      * Transport → Ride Share, Public Transit, Bike Share, Rail
      * Shopping → Marketplace, Retail, Electronics
      * Financial Services → Investment, FX Fee, Banking Fee
      * Travel → Airline, Hotel, Rail, Travel Services
      * Subscriptions → Cloud Storage, Music Streaming, Video Streaming
2. merchant_type
   * One of:
      * Brand
      * Individual
      * Financial Institution
      * Government
      * Nonprofit
      * Utility Provider
      * Unknown
3. recurring_candidate
   * true or false
   * Determine whether the transaction appears likely to recur based on merchant, amount patterns, subscription indicators, direct debit wording, standing orders, memberships, or common recurring services.
4. recurring_confidence
   * Decimal between 0 and 1.
5. spending_necessity
   * One of:
      * Essential
      * Lifestyle
      * Discretionary
6. location_hint
   * Infer location only when strongly indicated by transaction text.
   * Examples:
      * Manchester Airport
      * Toronto
      * London
   * Otherwise null.
7. travel_related
   * true or false
8. international_transaction
   * true or false
9. income_flag
   * true or false
10. transfer_flag

* true or false

11. anomaly_score

* Decimal between 0 and 1.
* Estimate how unusual this transaction appears relative to a typical consumer's spending.
* Large one-off investment transfers, unusually high spending, refunds, or foreign transactions may score higher.

12. insight_tags

* Array of short tags.
* Examples:
[
"subscription",
"investment",
"public_transit",
"airport_spend",
"international",
"refund",
"fuel"
]

13. merchant_normalization_notes

* A brief explanation of how the merchant was identified.


Example output:
{
"date": "2026-07-22",
"raw_description": "CARD PAYMENT TO Google One ON 21-07-2026",
"merchant": "Google One",
"category": "Subscriptions",
"subcategory": "Cloud Storage",
"merchant_type": "Brand",
"amount": -1.59,
"balance": 3259.42,
"confidence": 0.95,
"recurring_candidate": true,
"recurring_confidence": 0.99,
"spending_necessity": "Lifestyle",
"location_hint": null,
"travel_related": false,
"international_transaction": false,
"income_flag": false,
"transfer_flag": false,
"anomaly_score": 0.05,
"insight_tags": [
"subscription",
"cloud_storage",
"recurring"
],
"merchant_normalization_notes": "Recognized Google One subscription service."
}

## Libraries
The following libraries are used in the project:
os: Standard Python library for interacting with the operating system (used for environment variables and paths).

json: Standard Python library for parsing and working with JSON data.

fastapi: A modern, fast web framework used to build APIs (FastAPI, HTTPException).

pydantic: Data validation and settings management using Python type annotations (BaseModel).

CORSMiddleware: FastAPI middleware used to handle Cross-Origin Resource Sharing.

dotenv (python-dotenv): Library used to load environment variables from a .env file (load_dotenv).

openai: The official OpenAI Python SDK (OpenAI) used for LLM orchestration and tool calling.

backend.tools: Custom local module containing the tool definitions and dispatch mapping (TOOLS, TOOL_MAP).

streamlit: A Python framework used to build the interactive frontend user interface (st).

requests: HTTP library used to make API requests from the frontend to the backend.
