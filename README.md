# organization-insight
An application to find Companies,IPOs and Acquisitions

## Additional Information

1. This backend application uses FastAPI as the backend framework and PostgreSQL as the database.
2. Data is loaded from the following CSV files after minor cleanup:
    - `objects.csv`: Core data about companies
    - `ipos.csv`: Data about company IPOs
    - `acquisitions.csv`: Data about company acquisitions

## Technology/Language

- **Programming Language Used:** Python
- **Database:** PostgreSQL
- **Web Framework:** FastAPI
- **Other Python Packages Used:**
    1. SQLModel: A library for interacting with SQL databases from Python code using Python objects.
    2. Alembic: Used for handling database migration
- **Deployment:** Docker and Docker Compose

## Data Schema

There are three main entities: Company, Acquisitions, and IPOs. Company is related to Acquisitions and IPOs via foreign keys. Company name and country code are indexed for efficiency.

### Company

- **id (Primary Key)**
- entity_type
- entity_id
- **name (Index=True)**
- homepage_url
- overview
- **country_code (Index=True)**
- state_code
- city

### Acquisitions

- **id (Primary Key)**
- acquisition_id
- **acquiring_object_id (Foreign Key)**
- **acquired_object_id (Foreign Key)**
- price_amount
- price_currency_code
- acquired_at
- source_url
- source_description

### IPOs

- **id (Primary Key)**
- ipo_id
- **object_id (Foreign Key)**
- valuation_amount
- valuation_currency_code
- raised_amount
- raised_currency_code
- public_at
- stock_symbol
- source_url
- source_description

## API Endpoints

### Company List Page

1. **Get List of Companies**
    - **Method:** GET
    - **Endpoint:** /companies
    - **Description:** Retrieve a list of companies

2. **Get List of Companies Filtered By Company Name**
    - **Method:** GET
    - **Endpoint:** /companies?company_name={company_name}
    - **QueryString:** company_name={company_name}
    - **Description:** Retrieve a list of companies filtered by company name

3. **Get List of Companies Filtered By Country Code**
    - **Method:** GET
    - **Endpoint:** /companies?country_code={country_code}
    - **QueryString:** country_code={country_code}
    - **Description:** Retrieve a list of companies filtered by country code

4. **Get List of Companies Filtered By Having Made an Acquisition**
    - **Method:** GET
    - **Endpoint:** /companies?acquisitions={true}
    - **QueryString:** acquisitions=true
    - **Description:** Retrieve a list of companies that have made acquisitions

5. **Get List of Companies Filtered By Having Been Acquired**
    - **Method:** GET
    - **Endpoint:** /companies?acquired=true
    - **QueryString:** acquired=true
    - **Description:** Retrieve a list of companies that have been acquired

### Company Details Experience

This page provides the following information:

1. **Top-Level Data about the Company (website, description, etc)**
    - **Method:** GET
    - **Endpoint:** /companies/{company_id}
    - **Response:** (company_info)

2. **Whether the Company has Gone through an IPO, and Some Data Associated with the IPO if it Exists**
    - **Method:** GET
    - **Endpoint:** /companies/{company_id}/ipo_info
    - **Response:** {ipo_info}

3. **Whether the Company has Been Acquired, and Some Data Associated with the Acquisition if it Exists**
    - **Method:** GET
    - **Endpoint:** /companies/{company_id}/acquired_info
    - **Response:** {acquired_info}

4. **Whether the Company has Acquisitions, and Some Data Associated with the Acquisition(s) if they Exist**
    - **Method:** GET
    - **Endpoint:** /companies/{company_id}/acquisition_info
    - **Response:** {acquisition_info}

## Instructions to run locally

1. System should have `docker` and `docker-compose` installed
2. move to company-browser folder (root folder where docker-compose.yml file is located)
3. Run `docker-compose up --build`
4. Once both web and db started running the entrypoint script will run migrations + data upload + server startup
5. The server will be available on http://localhost:8000
6. To test the apis - swagger file is available on http://localhost:8000/docs
7. Each api endpoint can be tested from swagger file by clicking on `try it out` section in swagger endpoint and run `execute`

## test

1. Get companies with company Name filter: 
    
  `curl -X 'GET' \
  'http://localhost:8000/companies/?offset=0&limit=100&company_name=Apple' \
  -H 'accept: application/json'`

    Response: 
    [
    {
        "name": "Apple",
        "id": "c:1654",
        "homepage_url": "http://www.apple.com",
        "overview": "Apple Inc., formerly Apple Computer, Inc., is an American multinational corporation....",
        "country_code": "USA"
    }
    ]

2. Get Company Info
    `curl -X 'GET' \
  'http://localhost:8000/companies/c:1654' \
  -H 'accept: application/json'`

  Response: 
    [
    {
        "name": "Apple",
        "id": "c:1654",
        "homepage_url": "http://www.apple.com",
        "overview": "Apple Inc., formerly Apple Computer, Inc., is an American multinational corporation....",
        "country_code": "USA"
    }
    ]


3. Get IPO info
    `curl -X 'GET' \
  'http://localhost:8000/companies/c:1654/ipo_info' \
  -H 'accept: application/json'`
  Response:
  [
    {
        "valuation_amount": "0",
        "valuation_currency_code": "USD",
        "raised_amount": "0",
        "raised_currency_code": "USD",
        "public_at": "12/19/80",
        "stock_symbol": "NASDAQ:AAPL",
        "source_url": "",
        "source_description": "",
        "id": 1
    }
    ]

4. has been acquired ?
    `curl -X 'GET' \
  'http://localhost:8000/companies/c:1654/acquired_info' \
  -H 'accept: application/json'`
  Response: []

5. has acquisitions ?
    `curl -X 'GET' \
  'http://localhost:8000/companies/c%3A1654/acquisition_info' \
  -H 'accept: application/json'`

  Response: 

  [
  {
    "price_amount": "278000000",
    "price_currency_code": "USD",
    "acquired_at": "4/23/08",
    "source_url": "http://www.forbes.com/technology/2008/04/23/apple-buys-pasemi-tech-ebiz-cz_eb_0422apple.html",
    "source_description": "Apple Buys Chip Designer",
    "id": 259,
    "acquired_company": {
      "name": "PA Semi"
    }
  },
  {
    "price_amount": "0",
    "price_currency_code": "USD",
    "acquired_at": "10/16/06",
    "source_url": "http://www.macworld.com/article/53416/2006/10/silicon.html",
    "source_description": "Apple acquires Silicon Color",
    "id": 652,
    "acquired_company": {
      "name": "Silicon Color"
    }
  }
  ...
  ]

