import argparse
import datetime
from odysseus.webapp.data_aggregator import DataAggregator

from odysseus.city_data_manager.city_geo_trips.nyc_citi_bike_geo_trips import NewYorkCityBikeGeoTrips
from odysseus.city_data_manager.city_geo_trips.big_data_db_geo_trips import BigDataDBGeoTrips
from odysseus.city_data_manager.city_geo_trips.louisville_geo_trips import LouisvilleGeoTrips
from odysseus.city_data_manager.city_geo_trips.minneapolis_geo_trips import MinneapolisGeoTrips
from odysseus.city_data_manager.city_geo_trips.austin_geo_trips import AustinGeoTrips
from odysseus.city_data_manager.city_geo_trips.norfolk_geo_trips import NorfolkGeoTrips
from odysseus.city_data_manager.city_geo_trips.kansas_city_geo_trips import KansasCityGeoTrips
from odysseus.city_data_manager.city_geo_trips.chicago_geo_trips import ChicagoGeoTrips
from odysseus.city_data_manager.city_geo_trips.calgary_geo_trips import CalgaryGeoTrips
from odysseus.webapp.apis.api_cityDataManager.data_transormer_cdm.transformer_cdm import DataTransformer
from odysseus.webapp.apis.api_cityDataManager.utils import *

class CityDataManager():
    def __init__(self,cities=["Torino"], years=[2017], months=["10","11"], data_source_ids=["big_data_db"],collection="city_data_manager",dbhandler=None):
        self.cities = cities
        self.years = years
        self.months = months
        self.data_source_ids = data_source_ids
        self.data_agg = DataAggregator()
        self.dbhandler = dbhandler
        self.collection=collection
    def run(self):
        for city in self.cities:
            for data_source_id in self.data_source_ids:
                for year in self.years:
                    for month in self.months:
                        print(datetime.datetime.now(), city, data_source_id, year, month)

                        if data_source_id == "citi_bike":
                            geo_trips_ds = NewYorkCityBikeGeoTrips(year=int(year), month=int(month))

                        elif data_source_id == "big_data_db":
                            geo_trips_ds = BigDataDBGeoTrips(city, data_source_id, year=int(year), month=int(month))

                        elif data_source_id == "city_open_data":
                            if city == "city_of_louisville":
                                geo_trips_ds = LouisvilleGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_minneapolis":
                                geo_trips_ds = MinneapolisGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_austin":
                                geo_trips_ds = AustinGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_norfolk":
                                geo_trips_ds = NorfolkGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_kansas_city":
                                geo_trips_ds = KansasCityGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_chicago":
                                geo_trips_ds = ChicagoGeoTrips(year=int(year), month=int(month))

                            elif city == "city_of_calgary":
                                geo_trips_ds = CalgaryGeoTrips(year=int(year), month=int(month))

                        geo_trips_ds.get_trips_od_gdfs()
                        geo_trips_ds.save_points_data()
                        geo_trips_ds.save_trips()
                        
                        ###### QUANDO IL DB è FUNZIONANTE DECOMMENTA #######
                        cdm_path = set_path("city_data_manager")
                        filepath = os.path.join(
                            cdm_path,
                            city, "od_trips","trips",data_source_id, f"{year}_{month}","trips.csv"
                        )
                        doc_list=self.data_agg.groupby_day_hour(filepath,city)
                        agg_df = self.data_agg.spatial_grouping(filepath,city)
                        print("agg: ",agg_df)
                        spatial_doc = self.data_agg.build_spatial_doc(agg_df,city,data_source_id)
                        final_doc = []
                        for d in doc_list:
                            for s in spatial_doc:
                                docs = merge_documents(d,s)
                                if docs != None:
                                    final_doc.append(merge_documents(d,s))
                        print(final_doc)
                        for d in final_doc:
                            self.dbhandler.upload(d,self.collection)

        print(datetime.datetime.now(), "Done")

def merge_documents(doc1,doc2):
    if doc1["year"]==doc2["year"] and doc1["month"]==doc2["month"] and doc1["day"]==doc2["day"]:
        doc1.update(doc2)
        return doc1
    return None