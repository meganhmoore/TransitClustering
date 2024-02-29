import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN, HDBSCAN


def dbscan(point_df, map_df):
    coords_array = np.vstack([point_df.centroid.x, point_df.centroid.y]).T
    # Function DBSCAN is used to fit the clustering method to the coordinates
    # of the bus point data, with set values for Eps and MinPts:
    # After tuning, epsilon = 0.003 and min_samples of 10 worked best
    db_results = DBSCAN(eps=0.003, min_samples=10).fit(coords_array)

    # Creating a list with the clusters assignments and converting the labels
    # to string:
    db_labels = [str(label) for label in db_results.labels_]

    # Counting the number of resulting clusters in labels, ignoring noise if
    # present:
    n_clusters = len(set(db_labels)) - (1 if "-1" in db_labels else 0)

    # Counting the number of noise points:
    n_noise = db_labels.count("-1")

    print("Estimated number of clusters: %d" % n_clusters)
    print("Estimated number of noise points: %d" % n_noise)

    point_df["db_cluster"] = db_labels
    fig, ax = plt.subplots(figsize=(8, 8))
    map_df.plot(ax=ax, color="none", edgecolor="black")
    point_df.plot(column="db_cluster", ax=ax, cmap="viridis", markersize=3)
    plt.title("DBScan Bus Point Data")
    # plt.savefig("../../figures/dbscan_eps003minsamp10.png")
    plt.show()


def hdbscan(point_df, map_df):
    coords_array = np.vstack([point_df.centroid.x, point_df.centroid.y]).T
    # Function HDBSCAN is used to fit the clustering method to the coordinates
    # of our bus df with set value for min_cluster_size: 8 seemed to work best.
    hdb_results = HDBSCAN(min_cluster_size=8).fit(coords_array)

    # Creating a list with the clusters assignments and converting the labels
    # to string:
    hdb_labels = [str(label) for label in hdb_results.labels_]

    # Counting the number of resulting clusters in labels, ignoring noise if
    # present:
    n_clusters_ = len(set(hdb_labels)) - (1 if "-1" in hdb_labels else 0)

    # Counting the number of noise points:
    n_noise_ = hdb_labels.count("-1")

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)

    point_df["hdb_cluster"] = hdb_labels
    fig, ax = plt.subplots(figsize=(8, 8))
    map_df.plot(ax=ax, color="none", edgecolor="black")
    point_df.plot(
        column="hdb_cluster",
        ax=ax,
        cmap="viridis",
        legend=True,
        markersize=10,
        legend_kwds={"loc": "upper right", "title": "HDB_Cluster"},
    )
    plt.title("HDBScan Bus Point Data")
    # plt.savefig("../figures/hdbscan_mincluster8.png")
    plt.show()


def get_data():
    path = "~/Documents/spatial_clustering/final_project/data/"
    census_df = gpd.read_file(
        path + "census_tracts/geo_export_a19e0577-c0ec-456a-8bea-703d57c3459d.shp"
    )[["geoid10", "geometry"]]

    bus_point_df = gpd.read_file(path + "CTA_BusStops/CTA_BusStops.shp")

    chi_census = census_df.to_crs(bus_point_df.crs)

    return bus_point_df, chi_census


if __name__ == "__main__":
    bus_df, census_df = get_data()
    dbscan(bus_df, census_df)
    hdbscan(bus_df, census_df)
