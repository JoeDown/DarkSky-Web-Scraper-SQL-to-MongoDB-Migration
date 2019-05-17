import requests
import json
import os.path
import os
from os import getcwd
import time
import re
import sys
from helpers import *


# load_config will attempt to load a config from a given path
def load_config(path):
    if not re.match(r".+\.json$", path):
        return None, "%s is not a valid path to a json config" % path
    if not os.path.exists(path):
        return None, "%s is not a valid config path" % path
    with open(path, "r") as f:
        return json.load(f), None


def forge_darksky_url(key, lat, lon, time=0, exclude=None, units="auto"):
    # set time to current time if not is provided
    if time == 0:
        time = int(time.time())
    url_params = "?"
    # set exclusion params if any are provided
    exclude_str = "exclude="
    if not exclude is None:
        exclude_str += ",".join(exclude)+";"
    url_params += exclude_str + ";" + "units=" + units + ";"
    # forge the url and make the request
    url = "https://api.darksky.net/forecast/%s/%d,%d,%d%s"%(
        key,
        lat,
        lon,
        time,
        url_params,
    )
    return url

# request forcast data from darksky api and will return an error if any
def request_darksky(url):
    resp = None
    try:
        resp = requests.get(url)
    except:
        return None, "could not get from %s" % url
    if not resp.ok:
        return None, "response from %s had non-ok status code %s" % (url, resp.status_code)
    return resp, None

# save_response will create a new file and write response to it if no files exists.
# files that do exist will be overwritten unless specified.
def save_response(path, resp, overwrite=False):
    if not re.match(r".+\.json$", path):
        return "%s must be json file to write or create file at" % path
    filemode = "x"
    if os.path.exists(path):
        filemode = "w"
    if os.path.exists and overwrite == False:
        return "didn't write; overwrite false but file already exists"
    with open(path, filemode, encoding="utf-8") as f:
        f.write(json.dumps(resp.json(), indent=4))

# have_record_of will check to see if we already have the day saved
def have_record_of(time, path):
    if os.path.exists(path):
        return True
    return False

# precipitation_on will get the precipitation of a specified posix time
def precipitation_on(time, path):
    with open(path, "r") as f:
        result = None
        try:
            result = json.load(f)["daily"]["data"][0]["precipType"]
        except:
            result = "None"
        return result

# response_api_test will get the response from darksky api and check the error
def response_api_test():
    config, err = load_config("config.json")
    if err is not None:
        panic(err)
    key = config["key"]
    BERLIN_LAT = config["lat"]
    BERLIN_LON = config["lon"]
    exclusions = config["exclude"]
    units = config["units"]

    dark_sky_url = forge_darksky_url(
        key,
        BERLIN_LAT,
        BERLIN_LON,
        exclude=exclusions,
        units=units,
    )

    resp, err = request_darksky(dark_sky_url)
    if err is not None:
        panic(err)

    outfile_name = "expl_configed_resp.json"

    err = save_response(outfile_name, resp, overwrite=True)
    if err is not None:
        panic(err)

    if os.path.exists(outfile_name):
        print("test complete: successfully created file at %s/%s" % (getcwd(), outfile_name))
    else:
        print("test failed")
# response_api_test()
