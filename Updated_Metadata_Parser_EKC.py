## Metadata Parser Main Body of the code
## Author: Emily Coello

from pathlib import Path
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

data_dir = Path("./data")
output_dir = Path("./output")
output_file = output_dir / "combined_data.csv"


def unzip_all_files(zip_dir: Path):
    zip_files = list(zip_dir.glob("*.zip"))
    if not zip_files:
        print("No .zip files have been found to use, womp womp")
        return
    for zip_file in zip_files:
        extract_dir = zip_dir / zip_file.stem
        if extract_dir.exists():
            print(f"{extract_dir} already exists, skipping extraction")
        else:
            shutil.unpack_archive(zip_file, extract_dir)
            print(f"Extracted these files {zip_file} -> {extract_dir}")


def combine_csvs(data_dir: Path):
    dfs = []
    for csv_file in data_dir.glob("**/*.csv"):
        try:
            df = pd.read_csv(csv_file)
            df.columns = df.columns.str.strip()
            if 'id' in df.columns:
                df = df[df['id'] != 'id']
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    if not dfs:
        raise ValueError("No CSV files found or readable")
    combined_df = pd.concat(dfs, ignore_index=True, sort=True)


    # Flatten by patient ID I literally took this from Ruben's code and it fixed my code automatically
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
    if 'id' not in combined_df.columns:
        raise KeyError("Column 'id' not found for grouping")
    flattened_df = combined_df.groupby('id', as_index=False).apply(consolidate_group)
    return flattened_df


def cleaning_columns(df):
    if 'id' in df.columns:
        df['id'] = df['id'].astype(str).str.strip()
        df['id'] = df['id'].apply(lambda x: re.sub(r"[^P0-9]", "", x))
    return df


def filter_if_patient(df):
    if 'ancestor' not in df.columns:
        raise KeyError("WEEWOO This is not an ancestor!")
    df['is_patient'] = df['ancestor'].isna() | (df['ancestor'] == "")
    return df


def plot_data(df):
    output_dir.mkdir(parents=True, exist_ok=True)
    viable = df[df['is_patient']].copy()
    viable['age_years'] = pd.to_numeric(viable['age_years'], errors='coerce')

    sns.set_theme(style="whitegrid")

    # Age distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(viable['age_years'].dropna(), bins=20, color="pink", edgecolor="black")
    plt.title("Age Distribution of Patients")
    plt.savefig(output_dir / "age_distribution.png")
    plt.show()
    plt.close()

    # Sex distribution
    plt.figure(figsize=(6, 6))
    sns.countplot(x='sex_code', data=viable, palette="pastel")
    plt.title('Sex Distribution of Patients')
    plt.savefig(output_dir / "sex_distribution.png")
    plt.show()
    plt.close()

    # Pie chart to show how many patients vs ancestor there are
    viability_counts = df['is_patient'].value_counts()
    labels = ['Patients', 'Ancestors']
    sizes = [viability_counts.get(True, 0), viability_counts.get(False, 0)]
    colors = ['#ffb3ba', '#bae1ff']
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, wedgeprops=dict(edgecolor='black'))
    plt.title("Patient vs. Patient Ancestors")
    plt.savefig(output_dir / "patient_vs_ancestors_pie_chart.png")
    plt.show()
    plt.close()


def main():
    unzip_all_files(data_dir)
    df = combine_csvs(data_dir)
    df = cleaning_columns(df)
    df = filter_if_patient(df)
    output_dir.mkdir(parents=True, exist_ok=True)

    if 'deidentified_record_number' in df.columns:
        cols = list(df.columns)
        cols.insert(0, cols.pop(cols.index('deidentified_record_number')))
        df = df[cols]

    print(f"Wrote combined file to: {output_file}")
    df.to_csv(output_file, index=False)

    patients = df[df['is_patient']]
    ancestors = df[~df['is_patient']]
    patients.to_csv(output_dir / "actual_patients.csv", index=False)
    ancestors.to_csv(output_dir / "ancestors.csv", index=False)
    print(f"Saved {len(patients)} actual patients")
    print(f"Saved {len(ancestors)} patient ancestors")

    plot_data(df)
    print("Plots saved in:", output_dir)


if __name__ == "__main__":
    main()
