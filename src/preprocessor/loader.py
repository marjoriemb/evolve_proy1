import os
import pandas as pd

from .cleaner import dataframe_data_cleaner
from .cleaner import dataframe_loc_cleaner
from .cleaner import Statistics

from .transformer import transform_dataframe

def ValidateDirectory(folder):
    """
            Validate that `folder`, exists and is a directory.

            Args:
                folder (string): Folder to analyze.

            Return
                true if folder exists and is a directory, false otherwise.

            Raises:
                IOError: if src or dst are does not exist.
    """
    return os.path.exists(folder) and os.path.isdir(folder)

def load_and_clean_data(src, dst):
    """
        Load data from `src`, clean it and save it into `dst`.

        Args:
            src (string): Folder containing the data.
            dst (string): Output file path.

        Raises:
            IOError: if src or dst are does not exist.
    """

    if ValidateDirectory(src):
        if ValidateDirectory(os.path.dirname(dst)):

            filepath = os.path.join(src, "nomenclatura_2026_01.csv")
            locDf = pd.read_csv(filepath, encoding="ISO-8859-15")
            locDf.set_index('id', inplace=True)
            dataframe_loc_cleaner(locDf)
            locDf = locDf[['obcn']]

            stats = Statistics()
            transformed_data = pd.DataFrame()

            filenames = os.listdir(src)
            filenames.sort()
            filenames.remove("nomenclatura_2026_01.csv")
            for filename in filenames:
                print("Processing " + filename)
                filepath = os.path.join(src, filename)
                filepath = os.path.join(src, filename)
                df = pd.read_csv(filepath, parse_dates=['Inicio_del_viaje', 'Fin_del_viaje'], encoding="ISO-8859-15")
                df.set_index('Viaje_Id', inplace=True)

                stats += dataframe_data_cleaner(df, locDf)
                transform_dataframe(df, locDf)
                transformed_data = pd.concat([transformed_data, df])
                transformed_data = transformed_data[~transformed_data.index.duplicated(keep="first")]

            # Saving transformed dataset
            transformed_data.to_csv(dst)

            print ("Preprocessing complete")
            print ("    Statistics: ")
            print (f"        Trips processed: {stats.initial_rows_qty}")
            print (f"        Duplicated entries removed: {stats.duplicated_rows_removed}")
            print (f"        Rows with non valid values removed: {stats.rows_qty_after_na_removed + stats.rows_qty_after_remove_non_valid_gender}")
            print (f"        Marginal trips removed ( < 1 minute): {stats.rows_qty_after_marginals_trips}")
            print (f"        Trips associated with stations actually out of service: {stats.rows_qty_after_remove_non_valid_stations}")
            print (f"        Trips remaining after preprocessing: {stats.rows_qty}")

        else:
            IOError("dst must be a folder")
    else:
        raise IOError("src must be a folder")