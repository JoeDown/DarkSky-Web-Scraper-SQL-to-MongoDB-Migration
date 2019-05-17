import json
from helpers import *
from scraper import *
import pandas as pd
import time

# def load_config(path):
#     load_config(path)

# darksky_days will get all of the rainy days of a df from the darksky api
# it will create files in the directory
def darksky_days(df, config, date_format):
    key = config["key"]
    BERLIN_LAT = config["lat"]
    BERLIN_LON = config["lon"]
    exclusions = config["exclude"]
    units = config["units"]
    file_suffix = config["outfile_suffix"]
    out_directory = config["output_directory"].strip("/")

    if not os.path.exists(out_directory):
        panic("connot find directory: %s" % out_directory)

    df["Posix"] = df["Date"].apply(lambda x: to_posix(x, date_format))
    conditions = []
    for i, time in enumerate(df["Posix"]):
        outfile_name = out_directory + "/%d" % time + file_suffix + ".json"
        # check to see if a record exists for that day
        if have_record_of(time, outfile_name):
            # print("have record at %d" % time)
            conditions.append(precipitation_on(time, outfile_name))
            continue
        # make the url to query the api with
        dark_sky_url = forge_darksky_url(
            key,
            BERLIN_LAT,
            BERLIN_LON,
            time=time,
            exclude=exclusions,
            units=units,
        )
        # make the request and check the response for an error
        print("requesting %s" % dark_sky_url)
        resp, err = request_darksky(dark_sky_url)
        if err is not None:
            print(err)
            continue

        # create an outfile with a
        err = save_response(outfile_name, resp, overwrite=True)
        if err is not None:
            print(err)
            continue
        conditions.append(precipitation_on(time, outfile_name))
    df["Precipitation Type"] = pd.Series(conditions)
    return df

# darksky_days_test will test the package
def darksky_days_test():
    config, err = load_config("config.json")
    if err is not None:
        panic(err)

    df = pd.read_csv("2011_dates.csv")
    rainy_df = darksky_days(df, config,"%Y-%m-%d")
    print(rainy_df.head())

# usage will echo the "start scripting" usage
def usage():
    print('''
    config, err = load_config("your_config_here.json")
    if err is not None:
        panic(err)

    rainy_df = darksky_days(df, config,"%Y-%m-%d")
    print(rainy_df.head())
    ''')
# darksky_days_test()
