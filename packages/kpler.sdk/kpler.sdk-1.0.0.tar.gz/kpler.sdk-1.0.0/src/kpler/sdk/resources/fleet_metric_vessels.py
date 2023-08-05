from datetime import date
from enum import Enum
from typing import List, Optional

from kpler.sdk import Platform
from kpler.sdk.client import KplerClient
from kpler.sdk.configuration import Configuration
from kpler.sdk.exceptions import MaximumDaysPeriodExceededException
from kpler.sdk.helpers import process_date_parameter, process_enum_parameter, process_list_parameter


class FleetMetricVessels(KplerClient):

    """
    The ``FleetMetricVessels`` endpoint provides the list of vessels with their cargo per day on a given period,
    for the Floating Storage or the Loaded Vessels metrics, and their location.
    """

    RESOURCE_NAME = "fleet-metrics/vessels"

    AVAILABLE_PLATFORMS = [Platform.Liquids, Platform.LPG]

    def __init__(self, configuration: Configuration, column_ids: bool = True, log_level=None):
        super().__init__(configuration, self.AVAILABLE_PLATFORMS, column_ids, log_level)

    def get(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        zones: Optional[List[str]] = None,
        metric: Optional[Enum] = None,
        floating_storage_duration_min: Optional[str] = None,
        floating_storage_duration_max: Optional[str] = None,
        products: Optional[List[str]] = None,
        unit: Optional[Enum] = None,
    ):

        """

        Args:
            start_date: Optional[date] Start of the period (YYYY-MM-DD)
            end_date: Optional[date] End of the period (YYYY-MM-DD)
            zones: Optional[str] Names of countries/geographical zones
            metric: Optional[Enum] ``FleetMetricVesselsAlgo``
            floating_storage_duration_min: Optional[str] Minimum floating days [7-10-12-15-20-30-90]
            floating_storage_duration_max: Optional[str] Maximum floating days [10-12-15-20-30-90-Inf]
            products: Optional[str] Names of products
            unit: Optional[Enum] ``FleetMetricVesselsMeasurementUnit`` by default return in bbl unit

        Examples:

            >>>
            from datetime import date
            from kpler.sdk.resources.fleet_metric_vessels import FleetMetricVessels
            from kpler.sdk import FleetMetricVesselsAlgo,FleetMetricVesselsMeasurementUnit
            fleet_metric_vessels_client=FleetMetricVessels(config)
            fleet_metric_vessels_client.get(
                metric=FleetMetricVesselsAlgo.LoadedVessels,
                zones=["China"],
                start_date=date(2020,10,1),
                end_date=date(2020,10,31),
                floating_storage_duration_min="7",
                floating_storage_duration_max="10",
                products=["Dirty"],
                unit=FleetMetricVesselsMeasurementUnit.BBL
            )

            .. csv-table::
                :header:  "Date","IMO","Name","Dead Weight Tonnage","Quantity (bbl)","Family","Group","Product","Grade","Current Continent","..."

                "2020-10-01","9376749","Advantage Value","297557","1057204","Dirty","crude/co","crude","Iracema","Asia","..."
                "2020-10-01","9430313","Afra Royal","115948","530973","Dirty","crude/co","crude","Hamaca","Asia","..."
                "2020-10-01","9759836","Agios Sostis I","299983","2000003","Dirty","crude/co","crude","Arab Hy.","Asia","..."
                "2020-10-01","9653410","Al Derwazah","316884","2000003","Dirty","crude/co","crude","Kuwait","Asia","..."
                "2020-10-01","9329708","Al Jabriyah Ii","317570","2000003","Dirty","crude/co","crude","Kuwait","Asia","..."
                "...","...","...","...","...","...","...","...","...","...","..."
        """

        self.start_date = start_date
        self.end_date = end_date

        query_parameters = {
            "startDate": process_date_parameter(start_date),
            "endDate": process_date_parameter(end_date),
            "zones": process_list_parameter(zones),
            "metric": process_enum_parameter(metric),
            "floatingStorageDurationMin": floating_storage_duration_min,
            "floatingStorageDurationMax": floating_storage_duration_max,
            "products": process_list_parameter(products),
            "unit": process_enum_parameter(unit),
        }
        return self._get_dataframe(self.RESOURCE_NAME, query_parameters)

    def validate(self):
        if self.end_date and self.start_date:
            delta = (self.end_date - self.start_date).days  # type: ignore
            if delta >= 31:
                raise MaximumDaysPeriodExceededException()
