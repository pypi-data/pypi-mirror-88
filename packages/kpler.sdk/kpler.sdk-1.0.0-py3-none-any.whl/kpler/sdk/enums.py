from enum import Enum


class BallastCapacityPortCallsSources(Enum):
    """"""

    Forecast = "Forecast"  #:
    Market = "Market"  #:
    AIS = "AIS"  #:
    Port = "Port"  #:
    Analyst = "Analyst"  #:
    Fixture = "Fixture"  #:


class BallastCapacityPortCallsVesselStates(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:


class BallastCapacitySeriesPeriod(Enum):
    """"""

    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    Daily = "daily"  #:


class BallastCapacitySeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Country = "country"  #:
    Source = "source"  #:
    VesselType = "vesselType"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    VesselTypeOil = "vesselTypeOil"  #:


class BallastCapacitySeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class BallastCapacitySeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:
    Capacity = "capacity"  #:


class CongestionSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:
    EIA = "eia"  #:


class CongestionSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Port = "port"  #:
    Installation = "installation"  #:
    Country = "country"  #:
    VesselType = "vesselType"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselOperations = "VesselOperations"  #:
    WaitingStatus = "waitingStatus"  #:


class CongestionSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class CongestionSeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:
    Duration = "duration"  #:
    Capacity = "capacity"  #:


class CongestionSeriesOperation(Enum):
    """"""

    Load = "Load"  #:
    Discharge = "Discharge"  #:
    All = "All"  #:


class CongestionVesselsOperation(Enum):
    """"""

    Load = "Load"  #:
    Discharge = "Discharge"  #:
    All = "All"  #:


class Platform(Enum):
    """"""

    LNG = "https://api-lng.kpler.com/v1"  #:
    LPG = "https://api-lpg.kpler.com/v1"  #:
    Dry = "https://api-coal.kpler.com/v1"  #:
    Liquids = "https://api.kpler.com/v1"  #:


class TradeStatus(Enum):
    """"""

    Delivered = "delivered"  #:
    Scheduled = "scheduled"  #:
    Loading = "loading"  #:
    InTransit = "in transit"  #:


class FleetDevelopmentSeriesAggregationMetric(Enum):
    """"""

    Count = "count"  #:
    SumCapacity = "sumcapacity"  #:
    SumDeadWeight = "sumdeadweight"  #:


class FleetDevelopmentSeriesMetric(Enum):
    """"""

    Available = "available"  #:
    Deliveries = "deliveries"  #:
    Scrapping = "scrapping"  #:


class FleetDevelopmentSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Quarterly = "quarters"  #:


class FleetDevelopmentSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    ComplianceMethod = "complianceMethod"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:


class FleetDevelopmentSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class FlowDirection(Enum):
    """"""

    Import = "import"  #:
    Export = "export"  #:
    NetImport = "netimport"  #:
    NetExport = "netexport"  #:


class FlowSplit(Enum):
    """"""

    Total = "total"  #:
    Grades = "grades"  #:
    Products = "products"  #:
    OriginCountries = "origin countries"  #:
    DestinationCountries = "destination countries"  #:
    OriginInstallations = "origin installations"  #:
    DestinationInstallations = "destination installations"  #:
    VesselType = "vessel type"  #:
    TradeStatus = "trade status"  #:
    Sources = "sources "  #:
    Charterers = "charterers"  #:
    Routes = "routes"  #:
    Buyers = "buyer"  #:
    Sellers = "seller"  #:


class FlowPeriod(Enum):
    """"""

    Annually = "annually"  #:
    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    EiaWeekly = "eia-weekly"  #:
    Daily = "daily"  #:


class FlowMeasurementUnit(Enum):
    """"""

    KBD = "kbd"  #:
    BBL = "bbl"  #:
    KB = "kb"  #:
    MMBBL = "mmbbl"  #:
    MT = "mt"  #:
    KT = "kt"  #:
    T = "t"  #:
    CM = "cm"  #:


class FreightMetricSeriesMetric(Enum):
    """"""

    TonMiles = "TonMiles"  #:
    TonDays = "TonDays"  #:
    AvgSpeed = "AvgSpeed"  #:
    AvgDistance = "AvgDistance"  #:


class FreightMetricSeriesPeriod(Enum):
    """"""

    Monthly = "monthly"  #:
    Quarterly = "quarterly"  #:
    Annually = "annually"  #:


class FreightMetricSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    DestinationCountry = "destinationCountry"  #:
    OriginCountry = "originCountry"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    DestinationInstallation = "destinationInstallation"  #:
    OriginInstallation = "originInstallation"  #:
    DestinationSourceEta = "destinationSourceEta"  #:
    OriginSourceEta = "originSourceEta"  #:


class FreightMetricSeriesUnit(Enum):
    """"""

    MTNMI = "mt/nmi"  #:
    KTNMI = "kt/nmi"  #:
    TNMI = "t/nmi"  #:
    TDAY = "t/day"  #:
    KTDAY = "kt/day"  #:


class VesselTypesDry(Enum):
    """"""

    BabyCapes = "Baby Capes"  #:
    Capesize = "Capesize"  #:
    Handymax = "Handymax"  #:
    Handysize = "Handysize"  #:
    Newcastlemax = "Newcastlemax"  #:
    Kamsarmax = "Kamsarmax"  #:
    Panamax = "Panamax"  #:
    PostPanamax = "Post-Panamax"  #:
    Supramax = "Supramax"  #:
    Ultramax = "Ultramax"  #:
    Valemax = "Valemax"  #:
    VLOC = "VLOC"  #:


class VesselTypesLPG(Enum):
    """"""

    SGC = "SGC"  #:
    VLGC = "VLGC"  #:
    Handysize = "Handysize"  #:
    MGC = "MGC"  #:
    LGC = "LGC"  #:
    VLEC = "VLEC"  #:


class VesselTypesLNG(Enum):
    """"""

    XLUpperConventional = "XL (Upper Conventional)"  #:
    LLowerConventional = "L (Lower Conventional)"  #:
    QFlex = "Q-Flex"  #:
    XSPressureGas = "XS (Pressure Gas)"  #:
    MMedMax = "M (Med Max)"  #:
    SSmallSCale = "S (Small Scale)"  #:
    QMax = "Q-Max"  #:


class VesselTypesCPP(Enum):
    """"""

    LR2 = "LR2"  #:
    VLCC = "VLCC"  #:
    LR3 = "LR3"  #:
    MR = "MR"  #:
    GP = "GP"  #:
    LR1 = "LR1"  #:


class VesselTypesOil(Enum):
    """"""

    Aframax = "Aframax"  #:
    ProductTanker = "Product Tanker"  #:
    Suezmax = "Suezmax"  #:
    VLCC = "VLCC"  #:
    Panamax = "Panamax"  #:
    ULCC = "ULCC"  #:


class FleetDevelopmentVesselsComplianceMethods(Enum):
    """"""

    Scrubber = "Scrubber"  #:
    ScrubberPlanned = "Scrubber Planned"  #:
    ScrubberReady = "Scrubber Ready"  #:


class FleetDevelopmentVesselsMetric(Enum):
    """"""

    Available = "available"  #:
    Deliveries = "deliveries"  #:
    Scrapping = "scrapping"  #:


class FleetMetricAlgo(Enum):
    """"""

    FloatingStorage = "floating_storage"  #:
    LoadedVessels = "loaded_vessels"  #:


class FleetMetricPeriod(Enum):
    """"""

    Weekly = "weekly"  #:
    Daily = "daily"  #:
    EIA = "eia"  #:


class FleetMetricMeasurementUnit(Enum):
    """"""

    BBL = "bbl"  #:
    T = "t"  #:
    CM = "cm"  #:


class FleetMetricSplit(Enum):
    """"""

    Total = "total"  #:
    Grades = "grades"  #:
    Products = "products"  #:
    OriginCountries = "origin countries"  #:
    DestinationCountries = "destination countries"  #:
    OriginInstallations = "origin installations"  #:
    DestinationInstallations = "destination installations"  #:
    VesselType = "vessel type"  #:
    TradeStatus = "trade status"  #:
    Charterers = "charterers"  #:
    Buyer = "buyer"  #:
    Seller = "seller"  #:
    CurrentContinents = "current continents"  #:
    CurrentSubcontinents = "current subcontinents"  #:
    CurrentCountries = "current countries"  #:
    CurrentSubregions = "current subregions"  #:
    CurrentSeas = "current seas"  #:
    FloatingDays = "floating days"  #:


class FleetMetricVesselsAlgo(Enum):
    """"""

    FloatingStorage = "floating_storage"  #:
    LoadedVessels = "loaded_vessels"  #:


class FleetMetricVesselsMeasurementUnit(Enum):
    """"""

    BBL = "bbl"  #:
    KB = "kb"  #:
    MMBBL = "mmbbl"  #:
    MT = "mt"  #:
    KT = "kt"  #:
    T = "t"  #:
    CM = "cm"  #:


class OutageTypes(Enum):
    """"""

    Planned = "planned"  #:
    Unplanned = "unplanned"  #:


class PriceIndexes(Enum):
    """"""

    NBP = "NBP"  #:
    TTF = "TTF"  #:
    HenryHub = "Henry Hub"  #:
    SingaporeSling = "Singapore Sling"  #:
    NorthAsiaSling = "North Asia Sling"  #:
    DKISling = "DKI Sling"  #:
    RIMNEAsia = "RIM NE Asia"  #:
    Brent = "Brent"  #:
    JLC = "JLC"  #:
    JCC = "JCC"  #:


class ContractTypes(Enum):
    """"""

    SPA = "SPA"  #:
    TUA = "TUA"  #:
    LTA = "LTA"  #:
    Tender = "Tender"  #:


class FleetUtilizationSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:


class FleetUtilizationSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Product = "product"  #:
    State = "state"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:


class FleetUtilizationSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class FleetUtilizationSeriesVesselsState(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:


class FleetUtilizationSeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:


class FleetUtilizationVesselsState(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:


class FleetUtilizationVesselsUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class InventoriesPeriod(Enum):
    """"""

    Annually = "annually"  #:
    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    EiaWeekly = "eia-weekly"  #:
    Daily = "daily"  #:


class InventoriesSplit(Enum):
    """"""

    Total = "total"  #:
    ByCountry = "byCountry"  #:
    ByInstallation = "byInstallation"  #:
    ByPlayer = "byPlayer"  #:
    ByTankType = "byTankType"  #:
    ByOnshoreOffshoreStatus = "byOnshoreOffshoreStatus"  #:
