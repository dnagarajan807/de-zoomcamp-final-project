# Project:
---
Final Project for de-zoomcamp 2025 


# Project Summary:
---
This project will collect the housing market data for metropolitan areas, cities, neighborhoods and zip codes across the US from 2012 to till date, released by redfin. This weekly data will be updated every Wednesday with new data for the prior week. Using this data a investor can analyze what county, cities, or metros that has a good investment potential and identify what times in the year are good to buy or sell.


# Technologies to be Used:
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
The data for housing analysis is freely available from redfin, it is divided by region types and is in tsv format. 
- By combining all this data from 2012 for all region types there may be trends that can be identified which may otherwise be missed looking at a smaller subset of the data. 
- Creating a resilient data pipeline to facilitate the importing, aggregation of the data and presenting in dashboard will help investors analyse sold to list ratio and potential areas for investment opportunities.

# Data:
---
The data to be used for this project can be found below :

National data:- https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz
Metro data:- https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz
State data:- https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz
County data:- https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/county_market_tracker.tsv000.gz
City:- https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz

Below is a sample of the data to be used:
![Screenshot](/images/DataSample-FinalProject.png)

period_begin	Data collection being period	<br>
period_end	Data collection end period	<br>
period_duration	Data collection period duration	<br>
region_type	Region Type (County, Metro, State or City)	<br>
state_code	State code	<br>
property_type	Property type (Multihome, singlehome, Apartment or condo)	<br>
median_sale_price	Median sale price of the line item	<br>
median_sale_price_mom	Median sale price of the line item month over month	<br>
median_sale_price_yoy	Median sale price of the line item year over year	<br>
median_list_price	Median list prices of the line item	<br>
median_list_price_mom	Median list prices of the line item month over month	<br>
median_list_price_yoy	Median list prices of the line item year over year	<br>
homes_sold	No of homes sold	<br>
homes_sold_mom	No of homes sold month over month	<br>
homes_sold_yoy	No of homes sold year over year	<br>
pending_sales	No of homes pending sales	<br>
pending_sales_mom	No of homes pending sales month over month	<br>
pending_sales_yoy	No of homes pending sales year over year	<br>
new_listings	No of new listings	<br>
new_listings_mom	No of new listings month over month	<br>
new_listings_yoy	No of new listings year over year	<br>
inventory	Total no of inventory	<br>
inventory_mom	Total no of inventory month over month	<br>
inventory_yoy	Total no of inventory year over year	<br>
average_sale_to_list	Average sale to list ratio	<br>
average_sale_to_list_mom	Average sale to list ratio month over month	<br>
average_sale_to_list_yoy	Average sale to list ratio year over year	<br>
sold_above_list	Sold above list ratio	<br>
sold_above_list_mom	Sold above list ratio month over month	<br>
sold_above_list_yoy	Sold above list ratio year over year	<br>
off_market_in_two_weeks	off maket in two weeks (ratio)	<br>
off_market_in_two_weeks_mom	off maket in two weeks (ratio) month over month	<br>
off_market_in_two_weeks_yoy	off maket in two weeks (ratio) year over year	<br>



# Data Pipeline Diagram:
---
![Screenshot](/images/ProjectDataDiagram.jpeg)

# Data Visualizations
---
Data Visualizations for this project ccan be found here. https://lookerstudio.google.com/reporting/d2e46e03-9954-4671-9f0c-1a9783ef569c/page/p_3akvw4lzqd


# Steps to reproduce :
---
Follow the instructions [here](https://github.com/MichaelShoemaker/shoemaker-de-zoomcamp-final-project/blob/main/GitLikeMe.md)
# de-zoomcamp-final-project
