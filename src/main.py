## Metadata Parser Main Body of the code
## Author: Emily Coello

import os
import zipfile
import pandas as pd

data_dir = "../data"
output_file = "../output/combined_data.csv"

def unzip_all_files(zip_folder_path):
    for file in os.listdir(zip_folder_path):
        if file.endswith(".zip"):
            zip_path = os.path.join(zip_folder_path, file)
            extract_path = os.path.join(zip_folder_path, file.replace(".zip",""))
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Extracted these files {file} -> {extract_path}")

def combine_csvs(data_path):
    combined_df = pd.DataFrame()
    for root,_, files in os.walk(data_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path) #using pandas dataframes here
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                except Exception as e:
                    print(f"Uh oh, there's an error reading {file_path}: {e}")
    return combined_df

def main():
    unzip_all_files(data_dir)
    combined_df = combine_csvs(data_dir)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV written to: {output_file}")

if __name__ == "__main__":
    main()
                