#! /usr/bin/env python3

'''
Read the hourly weather forecast from Weather Underground and pretty print it
'''

import xdg.BaseDirectory
import os
import json


def hourly_forecast_report():
    # Prerequisite:
    # Download the hourly weather forecast data from
    # http://api.wunderground.com/api/Your_key/hourly/q/NJ/Hackensack.json
    # into ~/.cache/weather_underground/hourly/NJ/Hackensack.json
    fname = os.path.join(
        xdg.BaseDirectory.xdg_cache_home,
        'weather_underground',
        'hourly/NJ/Hackensack.json')  # implements BASEDIRSPEC
    fname = os.path.abspath(os.path.expanduser(fname))

    fhandle = open(fname, 'r')
    data = json.load(fhandle)

    hourly_forecast = data['hourly_forecast']

    delim = " "
    for hf in hourly_forecast:
        weekday = hf['FCTTIME']['weekday_name_abbrev']
        date = hf['FCTTIME']['year'] + '-' + \
            hf['FCTTIME']['mon_padded'] + '-' + \
            hf['FCTTIME']['mday_padded']

        # This will be something like "05:00 PM"
        time = hf['FCTTIME']['civil'].rjust(8)
        if (time == ' 8:00 AM' or time == ' 5:00 PM'):
            print()

        wx = hf['wx'].ljust(25)
        pop = hf['pop']

        line = weekday + delim + date + delim + \
            time + delim + wx + delim + pop
        print(line)


def main():
    hourly_forecast_report()


if __name__ == '__main__':
    main()


'''
Existing software survey:
https://github.com/dh4/pywu
Pros: code is easy to understand, lots of useful code to copy from
Cons: does not work with hourly forecasts
'''
