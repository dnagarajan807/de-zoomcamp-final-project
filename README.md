# Project:
---
Final Project for de-zoomcamp 2025 


# Project Summary:
---
This project will collect the housing market data for metropolitan areas, cities, neighborhoods and zip codes across the US from 2012 to till date, released by redfin. This weekly data will be updated every Wednesday with new data for the prior week. Using this data any investor can analyze what county, cities, or metros that has a good investment potential and identify what times in the year are good to buy or sell.


# Technologies Used:
---
- GCP VM Instance (Processing)
- Terraform (Infrastructure as a Service)
- Airflow (Data Pipeline - ETL)
- GCP Storage Bucket (Data Lake)
- Big Query (Data Warehouse)
- DBT (Creating Analytical Views)
- Google Data Studio (Dashboard)

# Problem Description:
---
The data for housing analysis is available for free from redfin, it is divided by region types and is in tsv format. 
- By automating and combining all this data from 2012 for all region types there may be trends that can be identified which may otherwise be missed looking at a smaller subset of the data. 
- Creating a resilient data pipeline to facilitate the importing, aggregation of the data and presenting in dashboard will help investors analyse median sales prices, median list prices, sold to list ratio, inventory and sold properties to identify potential areas for investment opportunities.

# Data:
---
The data to be used for this project can be found below :

#### National data:- "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz"<br>
#### Metro data:- "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz"<br>
#### State data:- "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz"<br>
#### County data:- "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/county_market_tracker.tsv000.gz"<br>
#### City:- "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz"<br>

Below is a sample of the data to be used:
![Screenshot](/images/sample_data.png)

period_begin	- Data collection being period	<br>
period_end	- Data collection end period	<br>
period_duration	- Data collection period duration	<br>
region_type	- Region Type (County, Metro, State or City)	<br>
state_code	- State code	<br>
property_type	- Property type (Multihome, singlehome, Apartment or condo)	<br>
median_sale_price	- Median sale price of the line item	<br>
median_sale_price_mom	- Median sale price of the line item month over month	<br>
median_sale_price_yoy	- Median sale price of the line item year over year	<br>
median_list_price	- Median list prices of the line item	<br>
median_list_price_mom	- Median list prices of the line item month over month	<br>
median_list_price_yoy	- Median list prices of the line item year over year	<br>
homes_sold	- No of homes sold	<br>
homes_sold_mom	- No of homes sold month over month	<br>
homes_sold_yoy	- No of homes sold year over year	<br>
pending_sales	- No of homes pending sales	<br>
pending_sales_mom	- No of homes pending sales month over month	<br>
pending_sales_yoy	- No of homes pending sales year over year	<br>
new_listings	- No of new listings	<br>
new_listings_mom	- No of new listings month over month	<br>
new_listings_yoy	- No of new listings year over year	<br>
inventory	- Total no of inventory	<br>
inventory_mom	- Total no of inventory month over month	<br>
inventory_yoy	- Total no of inventory year over year	<br>
average_sale_to_list	- Average sale to list ratio	<br>
average_sale_to_list_mom	- Average sale to list ratio month over month	<br>
average_sale_to_list_yoy	- Average sale to list ratio year over year	<br>
sold_above_list	- Sold above list ratio	<br>
sold_above_list_mom	- Sold above list ratio month over month	<br>
sold_above_list_yoy	- Sold above list ratio year over year	<br>
off_market_in_two_weeks	- off maket in two weeks (ratio)	<br>
off_market_in_two_weeks_mom	- off maket in two weeks (ratio) month over month	<br>
off_market_in_two_weeks_yoy	- off maket in two weeks (ratio) year over year	<br>



# Architecture Diagram:
---
![Screenshot](/images/Architecture.png)


# Steps to reproduce :

### Local setup
* Install the below tools:
  * [Terraform](https://www.terraform.io/downloads)
  * [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk#deb)
  * docker + docker-compose

### Cloud setup
* In GCP, create a service principal with the following permissions:
  * BigQuery Admin
  * Storage Admin
  * Storage Object Admin
  * Dataproc Admin
* Download the service principal authentication file and save it as `$HOME/.google/credentials/google_credentials_project.json`.


### Data Ingestion

* Setup airflow to perform data ingestion
* Create a google VM, and set up the private and public keys to remotely connect to the instance.
* After cloning the repo from "https://github.com/dnagarajan807/de-zoomcamp-final-project.git", sftp the top level folder and its contents into the instance.
* Go to de-zoomcamp-final-project and update the values shown below in the docker-compose file to match your environment
  
```shell
docker-compose build
docker-compose up airflow-init
docker-compose up -d
```

* Go to the aiflow UI at the web address `localhost:8080` and enable the `data_ingestion_gcs_dag`. 
* This dag will ingest the all 5 data files (.tsv) from redfin, upload it to the data lake as parquet and ingest it to the data warehouse staging tables.

### Initializing Infrastructure (Terraform)

* Perform the following to set up the required cloud infrastructure
```shell
cd terraform
terraform init
terraform plan
terraform apply

cd ..
```
* This will create the necessary gcs and bigquery instances.
![Screenshot](/images/gcs-screenshot.png)

![Screenshot](/images/bigquery-tables.png)

### Data Transformation
* Go to (https://github.com/dnagarajan807/final_project_dbt.git) and fork the repository.
* Create your project in cloud.getdbt.com, connect to your repository and to your bigquery connection.
* Run the below code
  
```shell
dbt deps
dbt run
```

* The transformed data and models will be saved as a Bigquery tables.
  
![Screenshot](/images/dbt-analytics-models.png)

![Screenshot](/images/dbt-run.png)

# Data Visualizations
---
Data Visualizations for this project ccan be found here. https://lookerstudio.google.com/reporting/d2e46e03-9954-4671-9f0c-1a9783ef569c/page/p_3akvw4lzqd

![Screenshot](/images/dashboard1.png)

![Screenshot](/images/dashboard2.png)


