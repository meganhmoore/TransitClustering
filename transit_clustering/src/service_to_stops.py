import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygeoda
from scipy.stats import poisson


def get_data(path: str = "~/Documents/spatial_clustering/final_project/data/"):
    """
    Read in census data, bus schedule data and bus stop point data.
    Also compute service by bus stop and by census tract (all bus stops in a
    tract).

    Inputs:
        path (str): path to read files from

    Returns:
        census_df (gpd.GeoDataFrame): census tract data
        bus_df_2 (gpd.GeoDataFrame): bus stop point data with added
            information about the number of service stops at each bus stop
            location (that are scheduled, not that necessarily actually occur)
        prob_census_df (pd.DataFrame): scheduled service to all bus stops in a
            census tract.
    """
    # get census data
    census_df = gpd.read_file(
        path + "census_tracts/geo_export_a19e0577-c0ec-456a-8bea-703d57c3459d.shp"
    )

    # get full bus schedule per week
    schedule_df = pd.read_csv(path + "google_transit/stop_times.txt")

    # get bus stop point data
    bus_point_df = gpd.read_file(path + "CTA_BusStops/CTA_BusStops.shp")
    bus_point_df["SYSTEMSTOP"] = bus_point_df["SYSTEMSTOP"].astype(int)

    stop_counts = schedule_df.groupby("stop_id").size().reset_index(name="stop_count")
    bus_df_2 = bus_point_df.copy()
    bus_df_2 = pd.merge(
        bus_df_2, stop_counts, how="inner", left_on="SYSTEMSTOP", right_on="stop_id"
    )

    stops_census = gpd.sjoin(bus_df_2, census_df, how="left", op="intersects")

    point_sum = (
        stops_census.groupby("geoid10")["stop_count"].sum().reset_index(name="count")
    )

    prob_census_df = census_df.merge(point_sum, how="left", on="geoid10").fillna(0)

    return census_df, bus_df_2, prob_census_df


def plot_service_by_stop(
    census_df: gpd.GeoDataFrame, bus_df: gpd.GeoDataFrame, save_fig: bool = False
):
    """
    Plot the bus stops and the density of service per bus stop point

    Inputs:
        census_df (gpd.GeoDataFrame): census tract data
        bus_df_2 (gpd.GeoDataFrame): bus stop point data with added
            information about the number of service stops at each bus stop
            location (that are scheduled, not that necessarily actually occur)
        save_fig (boolean): whether to save figures
    """
    # plot bus stops and the density of service per point
    census_df = census_df.to_crs(bus_df.crs)
    fig, ax = plt.subplots(figsize=(10, 15))
    census_df.plot(ax=ax, color="none", edgecolor="black")
    bus_df.plot(
        ax=ax,
        markersize=4,
        c=bus_df.stop_count,
        cmap="Greens",
        marker="o",
        legend=True,
        legend_kwds={"loc": "upper right"},
    )
    plt.title("Scheduled Service to each bus stop")
    if save_fig:
        plt.savefig("../figures/scheduled_bus_stops.png")
    plt.show()


def plot_service_density(prob_census_df, save_fig: bool = False):
    """
    Plot the expected and actual intensity of service to bus stops per census
    tract. This is a relatively simplistic interpretation of expectation since
    many other factors play into where we would expect demand to be highest
    (economic centers, transit hubs, etc), but this will be a starting point.

    Inputs:
        prob_census_df (pd.DataFrame): scheduled service to all bus stops in a
            census tract.
        save_fig (boolean): whether to save figures to file system
    """
    prob_census_df["area"] = prob_census_df.geometry.area / 10**6

    # compute intensity
    avg_intensity = prob_census_df["count"].sum() / prob_census_df["area"].sum()
    print("Average Intensity:", avg_intensity)

    # compute the expected number of points in each area
    prob_census_df["exppts"] = avg_intensity * prob_census_df["area"]

    # plot expectation
    fig, ax = plt.subplots()
    prob_census_df[["exppts", "geometry"]].plot("exppts", legend=True)
    if save_fig:
        plt.savefig("figures/balanced_census_bus.png")
    plt.show()

    prob_census_df["ptprob"] = poisson.pmf(
        prob_census_df["count"], prob_census_df["exppts"]
    )

    # compute variation from expectation with alpha = 0.01 because it seems to
    # be extremely variable
    conditions = [
        (prob_census_df["count"] > prob_census_df["exppts"])
        & (prob_census_df["ptprob"] < 0.01),
        (prob_census_df["count"] < prob_census_df["exppts"])
        & (prob_census_df["ptprob"] < 0.01),
    ]

    prob_census_df["prob_map"] = np.select(
        conditions,
        ["More than expected", "Less than expected"],
        default="Non-significant",
    )

    category_colors = {
        "More than expected": "plum",
        "Less than expected": "purple",
        "Non-significant": "whitesmoke",
    }
    fig, ax = plt.subplots(figsize=(20, 10))

    for category, color in category_colors.items():
        if category in list(prob_census_df["prob_map"].unique()):
            prob_census_df[prob_census_df["prob_map"] == category].plot(
                ax=ax, color=color, label=category, edgecolor="grey"
            )

    handles = [
        plt.Line2D(
            [0], [0], marker="o", color="w", markerfacecolor=color, markersize=10
        )
        for color in category_colors.values()
    ]
    labels = category_colors.keys()
    ax.legend(handles, labels, title="Probability Map", loc="upper right")
    if save_fig:
        plt.savefig("../figures/true_scheduled_bus_density.png")
    plt.show()


def plot_nuanced_service_densities(
    census_df: gpd.GeoDataFrame, bus_df: gpd.GeoDataFrame, save_fig: bool = False
):
    """
    Similar to the above function, but break the variance into further
    categories so we can see where service discrepancies are most extreme.

    Inputs:
        census_df (gpd.GeoDataFrame): census tract data
        bus_df_2 (gpd.GeoDataFrame): bus stop point data with added
            information about the number of service stops at each bus stop
            location (that are scheduled, not that necessarily actually occur)
        save_fig (boolean): whether to save figures to file system
    """
    census_bus_crs_df = census_df.to_crs(bus_df.crs)

    stops_census_df = gpd.sjoin(bus_df, census_bus_crs_df, how="inner", op="intersects")
    point_sum_df = (
        stops_census_df.groupby("geoid10")["stop_count"].sum().reset_index(name="count")
    )
    point_sum_df["count"] = point_sum_df["count"].astype(float)
    point_sum_gdf = gpd.GeoDataFrame(
        point_sum_df, geometry=gpd.GeoSeries(census_bus_crs_df["geometry"])
    )

    # create bins of service
    breaks15 = pygeoda.hinge15_breaks(point_sum_gdf["count"])

    fig, ax = plt.subplots(figsize=(10, 8))
    point_sum_gdf.plot(
        column="count",
        cmap="coolwarm_r",
        ax=ax,
        scheme="User_Defined",
        classification_kwds={"bins": breaks15},
    )
    # Add a colorbar
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap="coolwarm_r"), ax=ax)
    cbar.set_label("Bus Stop Service By Census Tract")
    plt.title("Bus Stop Service By Census Tract")
    if save_fig:
        plt.savefig("./figures/true_scheduled_bus_density_fromhinges.png")
    plt.show()


if __name__ == "__main__":
    census_df, bus_df, prob_census_df = get_data()
    plot_service_by_stop(census_df, bus_df)
    plot_service_density(prob_census_df)
    plot_nuanced_service_densities(census_df, bus_df)
