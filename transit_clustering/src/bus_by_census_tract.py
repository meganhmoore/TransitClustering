import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson


def get_census_and_bus_map(
    path: str = "~/Documents/spatial_clustering/final_project/data/",
    save_fig: bool = False,
):
    """
    Read in the census data, bus stop point location data and Chicago map
    to visualize the locations.

    Inputs:
        path (str): path to read files from
        save_fig (boolean): whether to save the figures to the file system
    """
    # get the census data
    census_df = gpd.read_file(
        path + "census_tracts/geo_export_a19e0577-c0ec-456a-8bea-703d57c3459d.shp"
    )

    # get the cta bus stop point data
    bus_point_df = gpd.read_file(path + "CTA_BusStops/CTA_BusStops.shp")

    # plot the basic map of bus stops
    census_df = census_df.to_crs(bus_point_df.crs)
    fig, ax = plt.subplots(figsize=(10, 15))
    census_df.plot(ax=ax, color="none", edgecolor="black")
    bus_point_df.plot(ax=ax, markersize=1, color="blue")
    if save_fig:
        plt.savefig("figures/census_bus.png")
    plt.show()

    return bus_point_df, census_df


def get_bus_density_by_census_tract(
    bus_df: gpd.GeoDataFrame, census_df: gpd.GeoDataFrame, save_fig: bool = False
):
    """
    Given the bus point data and the census tract geometries, compute the
    expected intensity of bus stop points, and plot how many stops we expect
    per tract to exist based on the area of each tract, then compute the
    actual number of stops and use a poisson distribution with alpha = 0.05 to
    determine which census tracts have statistically significantly more or
    less stops than expected.

    Inputs:
        bus_df (gpd.GeoDataFrame): bus point data
        census_df (gpd.GeoDataFrame): census tract geometries
        save_fig (boolean): whether to save the figures to the file system
    """
    bus_df = bus_df.to_crs(census_df.crs)
    bus_census = gpd.sjoin(bus_df, census_df, how="inner", op="intersects")

    point_sum = bus_census.groupby("geoid10").size().reset_index(name="count")

    prob_census_df = census_df.merge(point_sum, how="left", on="geoid10").fillna(0)

    # Area calculations
    prob_census_df["areakm2"] = prob_census_df.geometry.area / 10**6

    # Average Intensity
    avg_intensity = prob_census_df["count"].sum() / prob_census_df["areakm2"].sum()
    print("Average Intensity:", avg_intensity)

    # Expected number of points in each area
    prob_census_df["exppts"] = avg_intensity * prob_census_df["areakm2"]

    fig, ax = plt.subplots()
    prob_census_df[["exppts", "geometry"]].plot("exppts", legend=True, vmax=70)
    plt.title("Expected Bus Stop Count Per Tract")
    if save_fig:
        plt.savefig("figures/balanced_census_bus.png")
    plt.show()

    fig, ax = plt.subplots()
    prob_census_df[["count", "geometry"]].plot("count", legend=True, vmax=70)
    plt.title("Actual Bus Stop Count Per Tract")
    if save_fig:
        plt.savefig("figures/actual_bus_per_tract.png")
    plt.show()

    prob_census_df["ptprob"] = poisson.pmf(
        prob_census_df["count"], prob_census_df["exppts"]
    )

    conditions = [
        (prob_census_df["count"] > prob_census_df["exppts"])
        & (prob_census_df["ptprob"] < 0.05),
        (prob_census_df["count"] < prob_census_df["exppts"])
        & (prob_census_df["ptprob"] < 0.05),
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
    plt.savefig("figures/true_census_bus_density.png")
    plt.show()


if __name__ == "__main__":
    bus_df, census_df = get_census_and_bus_map()
    get_bus_density_by_census_tract(bus_df, census_df)
