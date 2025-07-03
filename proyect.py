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
import pandas as pd
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
        zip_name = os.path.splitext(os.path.basename(zip_file))[0]
        zip_output_dir = os.path.join(WORKING_DIR, zip_name)

        if not os.path.exists(zip_output_dir):
            os.makedirs(zip_output_dir)

        print(f"Extracting: {zip_file} into {zip_output_dir}")

        command = [r"C:\Program Files\7-Zip\7z.exe", "x", zip_file, f"-o{zip_output_dir}", "-y"]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error extracting {zip_file}:\n{result.stderr}")
            raise Exception(f"Failed to extract {zip_file}")

    print(f"All ZIPs have been extracted into subfolders inside: {WORKING_DIR}")

# -----------------------------
# 2️⃣ COMBINE CSV FILES
# -----------------------------

def combine_csv_files():
    """
    Concatenate all CSVs and consolidate rows by patient ID.
    """
    all_csv = glob.glob(os.path.join(WORKING_DIR, "**", "*.csv"), recursive=True)
    print(f"Found {len(all_csv)} CSV files.")

    if not all_csv:
        raise ValueError("No CSV files found.")

    df_list = [pd.read_csv(f) for f in all_csv]
    combined_df = pd.concat(df_list, ignore_index=True)

    combined_df.columns = [col.lower().strip() for col in combined_df.columns]

    if 'id' not in combined_df.columns:
        raise KeyError("Column 'id' not found in data.")

    def consolidate_group(group):
        combined = {}
        for col in group.columns:
            if pd.api.types.is_numeric_dtype(group[col]):
                combined[col] = group[col].max()
            else:
                combined[col] = group[col].dropna().astype(str).replace('', pd.NA).dropna().unique()
                if len(combined[col]) > 0:
                    combined[col] = combined[col][0]
                else:
                    combined[col] = pd.NA
        return pd.Series(combined)

    consolidated_df = combined_df.groupby('id', as_index=False).apply(consolidate_group)

    combined_path = os.path.join(WORKING_DIR, "combined_metadata.csv")
    consolidated_df.to_csv(combined_path, index=False)
    print(f"Combined file saved at: {combined_path}")

    return consolidated_df

# -----------------------------
# 3️⃣ FILTER AND EXCLUDE DATA
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

    type_clean = df[hist_type].fillna('').astype(str).str.lower().str.strip()
    detail_clean = df[hist_detail].fillna('').astype(str).str.lower().str.strip()

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
# 4️⃣ PLOTTING FUNCTIONS
# -----------------------------

def plot_relevant_data(df):
    """
    Generates relevant plots: medical history type distribution,
    exclusion status, and age distribution if available.
    """
    sns.set(style="whitegrid")

    # Plot 1: Medical history type distribution
    if 'medical_history_type' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(y=df['medical_history_type'].fillna('Unknown'), order=df['medical_history_type'].value_counts().index)
        plt.title("Distribution of Medical History Types")
        plt.xlabel("Number of Patients")
        plt.ylabel("Medical History Type")
        plt.tight_layout()
        plt.savefig(os.path.join(WORKING_DIR, "plot_medical_history_type.png"))
        plt.close()
        print("✅ Saved: plot_medical_history_type.png")

    # Plot 2: Excluded vs Not Excluded
    if 'Exclude' in df.columns:
        plt.figure(figsize=(6, 4))
        ax = sns.countplot(x=df['Exclude'])
        plt.title("Excluded vs Not Excluded Patients")
        plt.xlabel("Excluded")
        plt.ylabel("Number of Patients")
    
    # Add labels on top of bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(WORKING_DIR, "plot_excluded.png"))
    plt.close()
    print("✅ Saved: plot_excluded.png")

    # Plot 3: Age distribution
    age_col_candidates = [col for col in df.columns if 'age' in col]
    if age_col_candidates:
        age_col = age_col_candidates[0]
        plt.figure(figsize=(8, 5))
        sns.histplot(df[age_col].dropna(), bins=20, kde=True)
        plt.title(f"Age Distribution (column: {age_col})")
        plt.xlabel("Age")
        plt.ylabel("Number of Patients")
        plt.tight_layout()
        plt.savefig(os.path.join(WORKING_DIR, "plot_age_distribution.png"))
        plt.close()
        print("✅ Saved: plot_age_distribution.png")

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

    plot_relevant_data(marked_df)
    print(marked_df['Exclude'].value_counts())

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()



