"""
This script is provided by ChiHack Ghost Bus group,
it is not currently integrated into the data pipeline.

It will be the starting point for ingesting daily bus activity to compute
actual service and compare it to scheduled service.
"""

import pendulum
import pandas as pd

START_DATE = "2022-05-20"
END_DATE = "2022-05-21"

BUCKET_URL = "https://dmu5hq5f7fk32.cloudfront.net"


def get_data_and_write():
    start_date = pendulum.from_format(START_DATE, "YYYY-MM-DD", tz="America/Chicago")

    if END_DATE:
        end_date = pendulum.from_format(END_DATE, "YYYY-MM-DD", tz="America/Chicago")
    else:
        if pendulum.now("America/Chicago").hour >= 11:
            end_date = pendulum.yesterday("America/Chicago")
        else:
            end_date = pendulum.now("America/Chicago").subtract(days=2)

    date_list = [
        d.to_date_string() for d in pendulum.period(start_date, end_date).range("days")
    ]

    data_list = []
    errors_list = []

    for d in date_list:
        url = BUCKET_URL + f"/bus_full_day_data_v2/{d}.csv"
        print(f"{pendulum.now()}: processing {d} data")
        daily_data = pd.read_csv(url, low_memory=False)

        data_list.append(daily_data)

        print(f"{pendulum.now()}: processing {d} errors")
        daily_errors = pd.read_csv(
            (BUCKET_URL + f"/bus_full_day_errors_v2/{d}.csv"), low_memory=False
        )

        errors_list.append(daily_errors)

    data = pd.concat(data_list)
    errors = pd.concat(errors_list)
    print(errors)
    data.to_csv(f"../../data/ghost_bus_{START_DATE}.csv")


if __name__ == "__main__":
    get_data_and_write()
