import os

from preprocessor import load_and_clean_data
from analyzer import analyze_dataframe_and_save_pictures

if __name__ == '__main__':
    src = "../data/raw"
    dst = os.path.join("../data/processed", "transformed_data.csv")
    output = "../output"


    if not os.path.isfile(dst):
        print ("Loading and cleaning data...")
        load_and_clean_data(src, dst)
        print("Data loaded and processed")
    else:
        print("Warning: Transformed Data file exists. Avoiding Preprocessing!!!")


    analyze_dataframe_and_save_pictures(dst, output)