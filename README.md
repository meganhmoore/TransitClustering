# TransitClustering
TransitClustering: Mapping CTA Inequality in Chicago using geospatial clustering methods.

This is the code for the GISC Spatial Clustering course final project. It was primarily an exploratory project so code has not been fully productionized, see [Project Next Steps](#project-next-steps) for future work and steps to building it out. 

To read the final report, see `SpatialClusteringProject.pdf`

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
3. Exploratory work can be founnd in the notebooks, but each step of the analysis has been made into a script that can be found under  `transit_clustering/src`
3. To run the different analysis scripts, from the root directory run `python transit_clustering/src/<script>.py`

# Project Next Steps
New data:
* [Chicago ghost bus](https://ghostbuses.com/) data from Chi Hack Night would be extremely useful to measure the service that is actually ocurring rather than purely planned, as I hypothesize that some areas have more cancellations and failure of service than others
* Incorporate the L (CTA trains) to further explore the transit landscape and fill gaps.
* Commute data: this will be useful to understand current transit methods and where people are commuting to. I would be curious to understand commute patterns that do not match transit patterns (i.e. not commuting to or through economic centers), and I would like to get a sense of whether certain communities are utilizing transit but are suffering from slow/poor service or if communities have deserted transit altogether and use cars instead. 
* Reproduce analysis for other metropolitan areas (SF-BART, NYC-MTA, etc.)

This project is not yet productionized, to do this I would:
* Establish consistent data paths (internal to repo)
* Create scripts for downloading publically available data
* Add [click](https://click.palletsprojects.com/en/8.1.x/) so that stages can be run from the command line
* Add orchestration script to run the full data ingestion, analysis and produce reporting figures. 