import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygeoda
import statsmodels.api as sm

PATH = "~/Documents/spatial_clustering/final_project/data/"


def get_census_bus_data():
    # get census data
    census_df = gpd.read_file(
        PATH + "census_tracts/geo_export_a19e0577-c0ec-456a-8bea-703d57c3459d.shp"
    )

    # get full bus schedule per week
    schedule_df = pd.read_csv(PATH + "google_transit/stop_times.txt")

    # get bus stop point data
    bus_point_df = gpd.read_file(PATH + "CTA_BusStops/CTA_BusStops.shp")
    bus_point_df["SYSTEMSTOP"] = bus_point_df["SYSTEMSTOP"].astype(int)

    stop_counts = schedule_df.groupby("stop_id").size().reset_index(name="stop_count")
    bus_df_2 = bus_point_df.copy()
    bus_df_2 = pd.merge(
        bus_df_2, stop_counts, how="inner", left_on="SYSTEMSTOP", right_on="stop_id"
    )

    census_bus_crs_df = census_df.to_crs(bus_df_2.crs)

    stops_census_df = gpd.sjoin(
        bus_df_2, census_bus_crs_df, how="inner", op="intersects"
    )
    point_sum_df = (
        stops_census_df.groupby("geoid10")["stop_count"].sum().reset_index(name="count")
    )
    point_sum_df["count"] = point_sum_df["count"].astype(float)
    point_sum_gdf = gpd.GeoDataFrame(
        point_sum_df, geometry=gpd.GeoSeries(census_bus_crs_df["geometry"])
    )

    return point_sum_gdf, point_sum_df, census_df


def assess_socioecon_factor(
    point_sum_gdf, point_sum_df, census_df, socioec_df, socioec_col
):
    """
    Given a specific socioeconomic factor, clean, merge and run analysis.
    """

    census_tracts = list(point_sum_gdf.loc[:, "geoid10"].unique())
    socioec_df["tract"] = socioec_df["tract"].astype(str)
    chi_socio = socioec_df.loc[socioec_df.loc[:, "tract"].isin(census_tracts), :]

    socio_stats = pd.merge(
        chi_socio, point_sum_df, how="inner", left_on="tract", right_on="geoid10"
    )

    # plot across chicago
    socio_geo = census_df.merge(socio_stats[[socioec_col, "geoid10"]], on="geoid10")
    fig, ax = plt.subplots()
    socio_geo[[socioec_col, "geometry"]].plot(
        socioec_col, legend=True, vmax=0.2, vmin=-0.2
    )
    plt.title(f"{socioec_col} Rate Per Tract")
    # plt.savefig(f"../figures/{sociodem_col}_per_tract.png")
    plt.show()

    df_cleaned = socio_stats.dropna(subset=[socioec_col])
    X = df_cleaned["count"]
    y = df_cleaned[socioec_col]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    print(model.summary())


def run_regressions():
    """
    Get each socioeconomic factor, analyze, plot, and run a regression on bus
    service to determine if there is a statistically significant correlation.
    For now working with census tract level data on:
    1) Job growth
    2) Household income
    3) Incarceration
    """
    point_sum_gdf, point_sum_df, census_df = get_census_bus_data()
    employment = pd.read_csv(
        PATH + "demographics/tract_ann_avg_job_growth_2004_2013.csv"
    )
    employment_col = "Job_Growth_Rate_from_2004_to_2013"

    income = pd.read_csv(PATH + "demographics/tract_kfr_allSubgroups.csv")
    income_col = "kfr_rA_gP_pall"

    incarceration = pd.read_csv(PATH + "demographics/tract_jail_rP_gP_pall.csv")
    incarceration_col = "Incarceration_Rate_rP_gP_pall"

    assess_socioecon_factor(
        point_sum_gdf, point_sum_df, census_df, employment, employment_col
    )
    assess_socioecon_factor(point_sum_gdf, point_sum_df, census_df, income, income_col)
    assess_socioecon_factor(
        point_sum_gdf, point_sum_df, census_df, incarceration, incarceration_col
    )


if __name__ == "__main__":
    run_regressions()
