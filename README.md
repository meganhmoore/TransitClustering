# TransitClustering
TransitClustering: Mapping CTA Inequality in Chicago using geospatial clustering methods.


# Background 
Chicago has one of the busiest and most utilized public transit systems in the United States, providing 243.5 million rides in 2022 to a service community of 3.2 million people. And with an operating budget of nearly $2 billion, it has
a responsibility to serve Chicagoans effectively and equitably. Transit access has a huge impact on social mobility and access to opportunity (employment, education, social connection, etc) within a city and a lack of transit can have
lasting impact on people’s access to resources and opportunity. Additionally, there is strong evidence that the impact of redlining has lasting impacts today, and it is important to understand if transit is a victim of this perpetuation of inequities in Chicago.

This repository uses a series of geospatial clustering methods and statistics to combine a range of data sources and assess the state of equitable transit in Chicago.

# Data
* The main source of data is the [CTA Bus Stop point data](https://data.cityofchicago.org/Transportation/CTA-Bus-Stops-Shapefile/pxug-u72f/about_data) that contains all bus stops in Chicago. There are 10,760 bus stops recorded by the CTA.
* The second important source of data is the [Chicago census tract](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik) data that contains census tract boundaries and other levels of data such as community area. There are 801 census tracts in the Chicago area.
* To assess service, the [CTA GTFS feed](https://data.cityofchicago.org/Transportation/CTA-System-Information-Developer-Tool-GTFS-Data/sp6w-yusg/about_data) is used to gather scheduled bus service to each bus stop location each week. There are 2,663,183 schedule bus service stops per week.
* To compare to sociodemographic factors, we use the [Census](https://data.census.gov/table/ACSST1Y2022.S0802?q=United%20States&g=010XX00US_050XX00US17031) and [Opportunity atlas](https://www.opportunityatlas.org/) datasets that compile factors
such as household income, and education level across different geographic granularities (counties, tracts, etc.)
and for different demographic subgroups (black, white, female, male, etc.).
    1. Median household income in Chicago is $44k
    2. Median high school graduation rate is 86% (this is aggregated for the county so cannot be compared on a census tract basis)
    3. Median job growth rate from 2004-2013 in Chicago is -0.3%
    4. Median incarceration rate is 1.2%


Data is not made available in this repository but it is open source and should be accessible to all.

# Getting Started
This project uses poetry for python dependency management.
1. Make sure you have poetry installed in your virtual environment (`pip install poetry`)
2. Run `poetry install` and all dependencies will be installed in your environment
3. To run the different analysis scripts, from the root directory run `python transit_clustering/src/<script>.py`