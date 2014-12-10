import requests
from dateutil.parser import parse
from pprint import pprint
import time

class Plenario(object):

    API_URL = "http://plenar.io/v1/api/"

    DATASETS_ENDPOINT = "datasets"
    DETAIL_AGGREGATE = "detail-aggregate"
    WEATHER_DAILY = "weather/daily"
    WEATHER_HOURLY = "weather/hourly"

    OBS_DATE_START = "obs_date__ge"
    OBS_DATE_END = "obs_date__le"

    DATE_START = "date__ge"
    DATE_END = "date__le"

    DATETIME_START = "datetime__ge"
    DATETIME_END = "datetime__le"

    DATASETS = None

    def __init__(self):
        self.s = requests.session()

    def __get(self, endpoint, params = None):
        tries = 5

        while tries > 0:
            try:
                url = Plenario.API_URL + endpoint
                r = self.s.get(url, params=params)
                r = r.json()
                break
            except Exception, e:
                print "FAIL"
                tries -= 1
                time.sleep(1)
                if tries == 0:
                    raise e
        return (r["meta"], r["objects"])

    def get_datasets(self, force_reload = False):
        if Plenario.DATASETS is not None or force_reload:
            meta, objects = self.__get(Plenario.DATASETS_ENDPOINT)
            Plenario.DATASETS = dict([(d["dataset_name"], d) for d in objects])

        return Plenario.DATASETS


    def get_detail_aggregate(self, dataset, agg="day", from_date=None, to_date=None, field_filter={}):
        params = {}
        if from_date is not None:
            params[Plenario.OBS_DATE_START] = from_date
        if to_date is not None:
            params[Plenario.OBS_DATE_END] = to_date
        params["agg"] = agg
        params["dataset_name"] = dataset
        params.update(field_filter)

        meta, objects = self.__get(Plenario.DETAIL_AGGREGATE, params)

        r = [(parse(o["datetime"]), o["count"]) for o in objects]

        return r

    def get_weather_daily(self, station, from_date, to_date):
        params = {}
        params[Plenario.DATE_START] = from_date
        params[Plenario.DATE_END] = to_date
        params["wban_code"] = station

        meta, objects = self.__get(Plenario.WEATHER_DAILY, params)
        
        return objects[0]["station_info"], objects[0]["observations"]

    def get_weather_hourly(self, station, from_date, to_date):
        params = {}
        params[Plenario.DATETIME_START] = from_date
        params[Plenario.DATETIME_END] = to_date
        params["wban_code"] = station

        offset = 0
        done = False
        station_info = None
        observations = []

        while not done:
            params["offset"] = offset
            meta, objects = self.__get(Plenario.WEATHER_HOURLY, params)

            if len(objects) == 0:
                done = True
            else:
                o = objects[0]["observations"]
                station_info = objects[0]["station_info"]
                observations += o
                offset += len(o)
        
        return station_info, observations

    @staticmethod
    def get_weather_observations_list(observations, datefield, fields):
        return [ [parse(o[datefield])] + [o[f] for f in fields] for o in observations]
        


if __name__ == "__main__":

    p = Plenario()

    pprint(p.get_detail_aggregate(dataset = "311_service_requests_sanitation_code_complaints", 
                                  agg = "week",
                                  from_date = "2013-01-01", 
                                  to_date = "2013-12-31", 
                                  field_filter = {"ward": 2}))

    pprint(p.get_detail_aggregate(dataset = "crimes_2001_to_present", 
                                  agg = "week",
                                  from_date = "2013-01-01", 
                                  to_date = "2013-12-31", 
                                  field_filter = {"ward": 1}))

    si, o = p.get_weather_daily(14819, "2013-01-01", "2013-01-31")

    pprint(Plenario.get_weather_observations_list(o, ["temp_avg", "temp_min", "temp_max"]))

    si, o = p.get_weather_hourly(14819, "2013-01-01", "2013-03-31")




