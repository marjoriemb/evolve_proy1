
def transform_dataframe(df, locDf):
    """

        Get processed trips data and stations data and transform to perform Data Analyze

    :param df: Cleaned dataframe trips data
    :param locDf: Cleaned dataframe stations data
    :return: None
    """

    # Adding trip Duration column
    df["Duration"] = ((df["Fin_del_viaje"] - df["Inicio_del_viaje"]).dt.total_seconds() / 60).round().astype(int)

    # Removing the "Fin_del_viaje" column
    del df["Fin_del_viaje"]

    # Replacing "Origen_Id" and "Destino_Id" with the station name
    df["Origen"]  = df["Origen_Id"].map(locDf["obcn"])
    df["Destino"] = df["Destino_Id"].map(locDf["obcn"])
    df.drop(["Origen_Id", "Destino_Id"], axis=1, inplace=True)

    year_dataset = 2025
    # Adding Age column
    birthday_year_column = [name for name in df.columns.tolist() if name.endswith('_nacimiento')][0]
    df["Age"] = (year_dataset - df[birthday_year_column]).astype(int)

    # Removing column "Año_de_nacimiento"
    del df[birthday_year_column]

    # Removing "Usuario_Id" column
    del df["Usuario_Id"]