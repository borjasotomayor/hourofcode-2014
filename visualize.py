# -*- coding: utf-8 -*-

from regression import Regression
from plenario import Plenario
import itertools
import math
import sys
import numpy as np
import matplotlib
import matplotlib.pylab as plt


def fill_missing_values(l):
    for i, x in enumerate(l):
        if x is None:
            l[i] = (l[i-1] + l[i+1]) / 2

def get_chicago_crime_data(p, date_start, date_end, crime_types = None, wards = None):
    field_filter = {}

    if crime_types is not None:
        field_filter["primary_type__in"] = ",".join(crime_types)

    if wards is not None:
        field_filter["ward__in"] = ",".join([`w` for w in wards])

    dagg = p.get_detail_aggregate(dataset = "crimes_2001_to_present", 
                                  agg = "day",
                                  from_date = date_start, 
                                  to_date = date_end, 
                                  field_filter = field_filter)   

    return dagg

def get_chicago_weather_data(p, date_start, date_end):
    station_info, observations = p.get_weather_daily(94846, date_start, date_end)
    observations = Plenario.get_weather_observations_list(observations, "date", ["temp_avg"])
    observations.reverse()

    return observations

def get_crimes_label(crime_types):
    if crime_types is None:
        return "# of crimes"
    else:
        return "# of crimes (" + ", ".join(crime_types) + ")"

def plot_chicago_crime_weather(p, date_start, date_end, crime_types = None, wards = None):
    crime_data = get_chicago_crime_data(p, date_start, date_end, crime_types, wards)
    weather_data = get_chicago_weather_data(p, date_start, date_end)

    dates_crime = [x[0] for x in crime_data]
    dates_weather = [x[0] for x in weather_data]
    crimes = [x[1] for x in crime_data]
    temps = [x[1] for x in weather_data]

    fill_missing_values(temps)

    N = 30
    crimes_plt, = plt.plot(dates_crime, crimes, color="blue", label = get_crimes_label(crime_types) )
    weather_plt, = plt.plot(dates_weather, temps, color="green", label = u"Temperature (°F)")

    avg = matplotlib.mlab.movavg(crimes, N)
    plt.plot(dates_crime[N-1:], avg, color="blue", linewidth=3.0)

    avg = matplotlib.mlab.movavg(temps, N)
    plt.plot(dates_weather[N-1:], avg, color="green", linewidth=3.0)

    plt.legend(handles=[crimes_plt, weather_plt])
    plt.title("Weather and Crime in Chicago")
    plt.show()

def regression_chicago_crime_weather(p, date_start, date_end, crime_types = None, wards = None):
    crime_data = get_chicago_crime_data(p, date_start, date_end, crime_types, wards)
    weather_data = get_chicago_weather_data(p, date_start, date_end)

    crimes = [x[1] for x in crime_data]
    temps = [x[1] for x in weather_data]
    fill_missing_values(temps)
    
    r = Regression(temps, u"Temperature (°F)", crimes, get_crimes_label(crime_types))    
    r.compute()
    r.plot()

def pairs(lst):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item

def gen_happiness(temps, threshold):
    happiness = 0.0
    l = []
    for temp in temps:
        if temp >= threshold:
            happiness += (abs(threshold - temp))**2
        else:
            happiness -= (abs(threshold - temp))
        l.append(happiness)
    return l

def normalize_dates(d):
    first = d[0]
    return [(x - first).total_seconds() for x in d]

def plot_weather(p, ranges, plot_happiness = False, threshold=40.0):

    plts = []

    for date_start, date_end in ranges:
        print "Getting weather data for %s - %s..." % (date_start, date_end)
        station_info, observations = p.get_weather_hourly(94846, date_start, date_end)
        observations = Plenario.get_weather_observations_list(observations, "datetime", ["drybulb_fahrenheit"])
        observations.reverse()

        dates = [x[0] for x in observations]
        datesnorm = normalize_dates(dates)
        temps = [x[1] for x in observations]
        fill_missing_values(temps)


        label = "%s - %s" % (date_start, date_end)

        if plot_happiness:
            Ys = gen_happiness(temps, threshold)
        else:
            Ys = temps

        w_plt, = plt.plot(datesnorm, Ys, label=label)
        plts.append(w_plt)

    if plot_happiness:
        hline = 0
        title = "Weather-related Happiness in Chicago"
        ylabel = "Happiness"
    else:
        hline = 32
        title = "Temperatures in Chicago"
        ylabel = u"Temperature (°F)"

    xlabel = "Week"

    nweeks = (int(datesnorm[-1]) / 604800) + 1

    plt.xticks([w*604800 for w in range(nweeks)], [w for w in range(nweeks)])

    plt.axhline(hline, color="gray", linestyle="--")
    plt.legend(handles=plts, loc="lower left")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == "__main__":
    p = Plenario()

    if len(sys.argv) != 2:
        print "USAGE: python visualize.py TYPE_OF_PLOT"
        exit(1)

    plot = sys.argv[1]

    if plot == "crime_weather":
        plot_chicago_crime_weather(p, "2013-01-01", "2013-12-31", crime_types = ["THEFT"])
    elif plot == "crime_weather_regression":
        regression_chicago_crime_weather(p, "2013-01-01", "2013-12-31")
    elif plot == "winter_temp":
        plot_weather(p, ranges=( ("2013-01-01", "2013-04-01"), ("2014-01-01", "2014-04-01") ))
    elif plot == "winter_happiness":
        plot_weather(p, ranges=( ("2013-01-01", "2013-04-01"), ("2014-01-01", "2014-04-01") ), plot_happiness = True)
    else:
        print "Unknown plot type: " + plot
        exit(1)



