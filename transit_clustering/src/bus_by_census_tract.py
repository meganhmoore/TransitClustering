import geopandas as gpd
import matplotlib.pyplot as plt


def get_census_and_bus_map():
    # get the census data
    path = "~/Documents/spatial_clustering/final_project/data/"
    census_df = gpd.read_file(
        path + "census_tracts/geo_export_a19e0577-c0ec-456a-8bea-703d57c3459d.shp"
    )
    census_df.head(2)

    # get the cta bus stop point data
    bus_point_df = gpd.read_file(path + "CTA_BusStops/CTA_BusStops.shp")
    bus_point_df.head(5)

    # plot the basic map of bus stops
    census_df = census_df.to_crs(bus_point_df.crs)
    fig, ax = plt.subplots(figsize=(10, 15))
    census_df.plot(ax=ax, color="none", edgecolor="black")
    bus_point_df.plot(ax=ax, markersize=1, color="blue")
    plt.savefig("figures/census_bus.png")
    plt.show()


if __name__ == "__main__":
    get_census_and_bus_map()
