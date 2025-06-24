# main.py

"""
Python Summer 2025 Project
Author: Ruben Nunez
Supervisor: Emily Coello
Client: Sheridan Perry
Due date: June 23rd, 2025

Description:
This script combines all patient metadata CSV files into a single DataFrame,
filters based on medical history using keyword matching, excludes cases according
to specific criteria, and generates relevant medical visualizations.
"""

import os
import glob
import shutil
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

# -----------------------------
# PATH CONFIGURATION
# -----------------------------
ORIGINAL_ZIP_FOLDER = "D:\\Embry Riddle\\Python"
WORKING_DIR = "D:\\Embry Riddle\\Python"
OUTPUT_FILE = "combined_metadata.csv"
EXCLUSION_KEYWORDS = ["Leg"]  # Update according to your dictionary
MEDICAL_KEYWORDS = ["Broken"]  # Keywords of interest

# -----------------------------
# 1️⃣ PREPARE WORKING DIRECTORY
# -----------------------------

def prepare_working_directory():
    """
    Extract each ZIP into a unique subfolder using 7-Zip to avoid overwriting CSVs with the same name.
    """
    if not os.path.exists(WORKING_DIR):
        os.makedirs(WORKING_DIR)

    zip_files = glob.glob(os.path.join(ORIGINAL_ZIP_FOLDER, "*.zip"))

    for zip_file in zip_files:
        # Create a subfolder with the base name of the ZIP (without extension)
        zip_name = os.path.splitext(os.path.basename(zip_file))[0]
        zip_output_dir = os.path.join(WORKING_DIR, zip_name)

        if not os.path.exists(zip_output_dir):
            os.makedirs(zip_output_dir)

        print(f"Extracting: {zip_file} into {zip_output_dir}")

        # Exact path to your 7z.exe
        command = [r"C:\Program Files\7-Zip\7z.exe", "x", zip_file, f"-o{zip_output_dir}", "-y"]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error extracting {zip_file}:\n{result.stderr}")
            raise Exception(f"Failed to extract {zip_file}")

    print(f"All ZIPs have been extracted into subfolders inside: {WORKING_DIR}")


# -----------------------------
# 2️⃣ COMBINE CSVs
# -----------------------------

def combine_csv_files():
    """
    Merge all valid CSVs into a single DataFrame.
    Save the combined file in the working directory.
    """
    all_csv = glob.glob(os.path.join(WORKING_DIR, "**", "*.csv"), recursive=True)
    print(f"Found {len(all_csv)} CSV files.")

    if not all_csv:
        raise ValueError("No CSV files found.")

    df_list = [pd.read_csv(f) for f in all_csv]
    combined_df = pd.concat(df_list, ignore_index=True)

    combined_path = os.path.join(WORKING_DIR, "combined_metadata.csv")
    combined_df.to_csv(combined_path, index=False)
    print(f"Combined file saved at: {combined_path}")

    return combined_df


# -----------------------------
# 3️⃣ FILTER DATA BY KEYWORDS AND EXCLUSIONS
# -----------------------------

def mark_and_show_excluded(df):
    """
    Mark rows as 'Exclude' if:
    - 'medical_history_type' == 'Broken Bone'
    - AND 'medical_history_detail' contains 'Leg' (case-insensitive)

    Display and save these rows.
    """
    df.columns = [col.lower().strip() for col in df.columns]
    print("Normalized columns:", df.columns.tolist())

    hist_type = 'medical_history_type'
    hist_detail = 'medical_history_detail'

    if hist_type not in df.columns or hist_detail not in df.columns:
        raise KeyError(f"Required columns not found: '{hist_type}', '{hist_detail}'")

    # Normalize
    type_clean = df[hist_type].fillna('').astype(str).str.lower().str.strip()
    detail_clean = df[hist_detail].fillna('').astype(str).str.lower().str.strip()

    # ✅ EXCLUDE: Broken Bone AND Leg in detail
    condition_exclude = (type_clean == 'broken bone') & detail_clean.str.contains('leg', case=False, na=False)

    df['Exclude'] = condition_exclude

    excluded_df = df[df['Exclude']]
    print(f"\n=== EXCLUDED ROWS (type == 'Broken Bone' AND detail contains 'Leg') ===")
    print(excluded_df[['id', 'medical_history_type', 'medical_history_detail']])

    excluded_path = os.path.join(WORKING_DIR, "excluded_metadata.csv")
    excluded_df.to_csv(excluded_path, index=False)
    print(f"Total excluded rows: {excluded_df.shape[0]}")
    print(f"Excluded file saved at: {excluded_path}")

    return df


# -----------------------------
# 5️⃣ MAIN PIPELINE
# -----------------------------

def main():
    prepare_working_directory()
    combined_df = combine_csv_files()
    marked_df = mark_and_show_excluded(combined_df)

    combined_with_exclude_path = os.path.join(WORKING_DIR, "combined_with_exclude.csv")
    marked_df.to_csv(combined_with_exclude_path, index=False)
    print(f"Final file with 'Exclude' column saved at: {combined_with_exclude_path}")

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

