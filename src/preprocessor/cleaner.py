import pandas as pd


class Statistics:
    def __init__(self):
        self.__rows_qty = 0
        self.__duplicated_rows_removed_qty = 0
        self.__rows_qty_after_na_removed = 0
        self.__rows_qty_after_marginals_trips = 0
        self.__rows_qty_after_remove_non_valid_gender = 0
        self.__rows_qty_after_remove_non_valid_stations = 0

    def add_rows_qty(self, rows_qty):
        self.__rows_qty += rows_qty

    def add_duplicated_rows_qty_removed(self, rows_qty):
        self.__duplicated_rows_removed_qty += rows_qty

    def add_na_rows_qty_removed(self, rows_qty):
        self.__rows_qty_after_na_removed += rows_qty

    def add_margin_rows_qty_removed(self, rows_qty):
        self.__rows_qty_after_marginals_trips += rows_qty

    def add_no_valid_gender_rows_qty_removed(self, rows_qty):
        self.__rows_qty_after_remove_non_valid_gender += rows_qty

    def add_no_valid_stations_rows_qty_removed(self, rows_qty):
        self.__rows_qty_after_remove_non_valid_stations += rows_qty

    def __rows_removed(self):
        return  self.__duplicated_rows_removed_qty + \
                self.__rows_qty_after_na_removed + \
                self.__rows_qty_after_marginals_trips + \
                self.__rows_qty_after_remove_non_valid_gender + \
                self.__rows_qty_after_remove_non_valid_stations

    @property
    def rows_qty(self):
        return self.__rows_qty - self.__rows_removed()

    @property
    def initial_rows_qty(self):
        return self.__rows_qty

    @property
    def rows_qty_after_na_removed(self):
        return self.__rows_qty_after_na_removed

    @property
    def rows_qty_after_marginals_trips(self):
        return self.__rows_qty_after_marginals_trips

    @property
    def rows_qty_after_remove_non_valid_gender(self):
        return self.__rows_qty_after_remove_non_valid_gender

    @property
    def rows_qty_after_remove_non_valid_stations(self):
        return self.__rows_qty_after_remove_non_valid_stations

    @property
    def duplicated_rows_removed(self):
        return self.__duplicated_rows_removed_qty

    def __iadd__(self, other):
        self.__rows_qty += other.__rows_qty
        self.__duplicated_rows_removed_qty += other.__duplicated_rows_removed_qty
        self.__rows_qty_after_na_removed += other.__rows_qty_after_na_removed
        self.__rows_qty_after_marginals_trips += other.__rows_qty_after_marginals_trips
        self.__rows_qty_after_remove_non_valid_gender += other.__rows_qty_after_remove_non_valid_gender
        self.__rows_qty_after_remove_non_valid_stations += other.__rows_qty_after_remove_non_valid_stations

        return self

def dataframe_data_cleaner(df, locDf):
    """
        Clean a dataframe for Data Analysis

    :param df: Dataframe to analyze
    :param locDf: Dataframe containing all valid locations
    :return: An Statistics object with feedback of the cleaning process.
    """

    stats = Statistics()
    stats.add_rows_qty(len(df))

    # Removing duplicated rows
    df.drop_duplicates(inplace=True)
    stats.add_duplicated_rows_qty_removed(stats.rows_qty - len(df))

    # Removing rows with missing data
    df.dropna(inplace=True)
    stats.add_na_rows_qty_removed(stats.rows_qty - len(df))
    df.query("Genero in ['M', 'F']", inplace=True)
    stats.add_no_valid_gender_rows_qty_removed(stats.rows_qty - len(df))

    # Removing marginal trips, (less <= 1m)
    df.query("(Fin_del_viaje - Inicio_del_viaje) > @pd.Timedelta(minutes=1)", inplace=True)
    stats.add_margin_rows_qty_removed(stats.rows_qty - len(df))

    # Removing trips with no valid Stations
    valid_locs = locDf.index
    df.query("Origen_Id in @valid_locs and Destino_Id in @valid_locs", inplace=True)
    stats.add_no_valid_stations_rows_qty_removed(stats.rows_qty - len(df))

    return stats

def dataframe_loc_cleaner(locs):
    """
        Clean the locations dataframe for Data Analysis
        Remove all stations that are not in Service

    :param locs: Dataframe containing locations
    :return: None
    """
    locs.query("status == 'IN_SERVICE'", inplace=True)
    locs.dropna(inplace=True)
    locs.drop_duplicates(inplace=True)
