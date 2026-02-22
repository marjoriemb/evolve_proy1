import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def TripsByAgeGroupAndWeekDay(df, output):
    picture_filename = os.path.join(output,"trips_by_age_and_week_day.png")
    if not os.path.isfile(picture_filename):
        bins = [0, 18, 30, 45, 60, 200]
        labels = ["0-17", "18-29", "30-44", "45-59", "60+"]
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = (
            df
            .assign(
                Age_Group=lambda x: pd.cut(x["Age"], bins=bins, labels=labels, right=False),
                Week_Day=lambda x: x["Inicio_del_viaje"].dt.day_name()
            )
            .assign(
                Week_Day=lambda x: pd.Categorical(x["Week_Day"], categories=days_order, ordered=True)
            )
            .groupby(["Week_Day", "Age_Group"])
            .size()
            .reset_index(name="Cantidad")
            .pivot(index="Age_Group", columns="Week_Day", values="Cantidad")
        )

        pivot.loc["Total"] = pivot.sum()

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, cmap="Blues", fmt="d")
        plt.title("Trips by age group and day of the week")
        plt.ylabel("Age Group")
        plt.xlabel("Day of the week")
        plt.xticks(rotation=45)
        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")

def TripsByAgeGroupAndGender(df, output):
    picture_filename = os.path.join(output, "trips_by_age_and_sex.png")
    if not os.path.isfile(picture_filename):
        bins = [0, 18, 30, 45, 60, 200]
        labels = ["0-17", "18-29", "30-44", "45-59", "60+"]
        tabla = (df.assign(Age_Group=lambda x: pd.cut(x["Age"], bins=bins, labels=labels, right=False)).groupby(
            ["Genero", "Age_Group"]).size().reset_index(name="Qty"))
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=tabla, x="Genero", y="Qty", hue="Age_Group", palette="Blues")
        ax.set_xlabel("Sex")
        ax.set_ylabel("Trips")
        ax.legend(title="Age")
        plt.title("Trips by age and sex")
        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")

def DurationMeanByAgeGroupAndGender(df, output):
    picture_filename = os.path.join(output, "duration_mean_by_age_group_and_gender.png")
    if not os.path.isfile(picture_filename):
        bins = [0, 18, 30, 45, 60, 200]
        labels = ["0-17", "18-29", "30-44", "45-59", "60+"]

        table = (
                df
                .assign(
                    Age_Group=lambda x: pd.cut(x["Age"], bins=bins, labels=labels, right=False)
                )
                .groupby(["Genero", "Age_Group"])["Duration"]
                .mean().reset_index()
        )

        pivot = table.pivot(index="Age_Group", columns="Genero", values="Duration")

        pivot["Total"] = pivot.mean(axis=1)
        row_total = pivot.mean(axis=0)
        pivot.loc["Total"] = row_total
        plt.figure(figsize=(8, 6))
        sns.heatmap(pivot, annot=True, cmap="Blues",
                    fmt=".1f" )

        plt.title("Trip duration average by sex and age")
        plt.xlabel("Sex")
        plt.ylabel("Age")
        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")

def TripsBetweenStations(df, output):
    picture_filename = os.path.join(output, "trips_between_stations.png")
    if not os.path.isfile(picture_filename):
        orig = df["Origen"].to_numpy()
        dest = df["Destino"].to_numpy()

        A = np.minimum(orig, dest)
        B = np.maximum(orig, dest)

        df2 = pd.DataFrame({"A": A, "B": B})

        table = (
            df2.groupby(["A", "B"])
            .size()
            .reset_index(name="Qty")
        )

        top10 = table.sort_values("Qty", ascending=False).head(10)

        top10["Pair"] = top10["A"] + " — " + top10["B"]

        plt.figure(figsize=(14, 8))
        sns.barplot(
            data=top10,
            x="Qty",
            y="Pair",
            color="royalblue"
        )

        plt.title("Most frequent trips")
        plt.xlabel("Trips")
        plt.ylabel("Stations")
        plt.tight_layout()
        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")

def TripsByHoursAndGender(df, output):
    picture_filename = os.path.join(output, "trips_by_hours_and_gender.png")
    if not os.path.isfile(picture_filename):
        df["Hora"] = df["Inicio_del_viaje"].dt.hour

        bins = list(range(0, 25, 3))
        labels = [f"{h:02d}-{h + 3:02d}" for h in bins[:-1]]

        df["Franja3h"] = pd.cut(df["Hora"], bins=bins, labels=labels, right=False)

        tabla = df.groupby(["Franja3h", "Genero"]).size().reset_index(name="Cantidad")

        plt.figure(figsize=(14, 6))
        ax = sns.barplot( data=tabla, x="Franja3h", y="Cantidad", hue="Genero", palette="Set2" )

        ax.legend(title="Gender")
        plt.title("Trips by Hours")
        plt.xlabel("Hours")
        plt.ylabel("Trips")

        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")

def TripsByHoursAndAge(df, output):
    picture_filename = os.path.join(output, "trips_by_hours_and_age.png")
    if not os.path.isfile(picture_filename):
        df["Hour"] = df["Inicio_del_viaje"].dt.hour

        bins_franjas = list(range(0, 25, 3))  # [0,3,6,...,24]
        labels_franjas = [f"{h:02d}-{h + 3:02d}" for h in bins_franjas[:-1]]

        df["Franja3h"] = pd.cut(df["Hour"], bins=bins_franjas, labels=labels_franjas, right=False)

        bins = [0, 18, 30, 45, 60, 200]
        labels = ["0-17", "18-29", "30-44", "45-59", "60+"]

        df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

        tabla = df.groupby(["Franja3h", "AgeGroup"]).size().reset_index(name="Qty")

        plt.figure(figsize=(14, 6))
        ax = sns.barplot(
            data=tabla,
            x="Franja3h",
            y="Qty",
            hue="AgeGroup",
            palette="bright"
        )

        ax.legend(title="Age")

        plt.title("Trip by Hours and Age")
        plt.xlabel("Hours")
        plt.ylabel("Trips")
        plt.tight_layout()
        plt.savefig(picture_filename, dpi=600, bbox_inches="tight")


def analyze_dataframe_and_save_pictures(csv, output):
    """
        Analyze the dataframe and save the pictures.

    :param csv: Path to the csv file
    :param output: Directory to save the pictures
    :return: None
    """

    if os.path.isfile(csv):
        if os.path.isdir(output):
            df = pd.read_csv(csv, parse_dates=['Inicio_del_viaje'])

            TripsByAgeGroupAndWeekDay(df, output)

            TripsByAgeGroupAndGender(df, output)

            DurationMeanByAgeGroupAndGender(df, output)

            TripsBetweenStations(df, output)

            TripsByHoursAndGender(df, output)

            TripsByHoursAndAge(df, output)

        else:
            raise IOError("Output parameter is not a directory")
    else:
        raise IOError("The csv file does not exist")