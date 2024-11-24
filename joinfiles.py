import os
import json
import pandas as pd


def load_config(config_path="config.json"):
    """
    Load the configuration file.
    """
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}")
        return None


def load_files(source_directory, csv_delimiter=","):
    """
    Load files from the source directory, check formats, and skip empty files.
    """
    if not os.path.exists(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        return []

    files = os.listdir(source_directory)
    if not files:
        print("No files found in the source directory.")
        return []

    supported_formats = ('.csv', '.xlsx', '.xls')
    data_frames = []

    print("Checking files in the source directory...")
    for file in files:
        file_path = os.path.join(source_directory, file)
        if file.lower().endswith(supported_formats):
            try:
                if file.lower().endswith('.csv'):
                    data = pd.read_csv(file_path, delimiter=csv_delimiter)
                else:
                    data = pd.read_excel(file_path)

                if data.empty:
                    print(f"Skipping empty file: {file}")
                else:
                    print(f"Loaded file: {file} (Rows: {data.shape[0]}, Columns: {data.shape[1]})")
                    data['source_file'] = file
                    data_frames.append(data)
            except Exception as e:
                print(f"Error processing file '{file}': {e}")
        else:
            print(f"Skipping unsupported file format: {file}")
    
    return data_frames


def validate_and_transform(data_frames):
    """
    Validate and transform the input DataFrames based on user-defined column types.
    """
    if not data_frames:
        print("No data available for validation and transformation.")
        return []

    # Use the first DataFrame's columns as the basis for all transformations
    print("\nStandardize Column Data Types:")
    sample_data = data_frames[0]
    sample_data.columns = [col.strip().lower().replace(" ", "_") for col in sample_data.columns]
    
    column_types = {}
    for col in sample_data.columns:
        print(f"Column '{col}' detected type: {sample_data[col].dtype}")
        user_input = input(f"Specify data type for '{col}' (int, float, str, date) | leave blank for default: ").strip().lower()
        column_types[col] = user_input

    # Apply transformations to all DataFrames
    transformed_data_frames = []
    for df in data_frames:
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        for col, col_type in column_types.items():
            if col in df.columns:
                if col_type == "int":
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                elif col_type == "float":
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
                elif col_type == "str":
                    df[col] = df[col].astype(str)
                elif col_type == "date":
                    df[col] = pd.to_datetime(df[col], errors='coerce')
        transformed_data_frames.append(df)

    return transformed_data_frames


def merge_files(data_frames, output_directory, output_filename):
    """
    Merge DataFrames and save the result.
    """
    if not data_frames:
        print("No valid data to merge.")
        return

    merged_data = pd.concat(data_frames, ignore_index=True)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Prompt user to choose the output file format
    while True:
        file_format = input("Choose output file format (csv/excel): ").strip().lower()
        if file_format in ["csv", "excel"]:
            break
        else:
            print("Invalid choice. Please enter 'csv' or 'excel'.")

    if file_format == "csv":
        output_path = os.path.join(output_directory, output_filename)
        merged_data.to_csv(output_path, index=False)
    else:  # Excel format
        output_path = os.path.join(output_directory, output_filename.replace('.csv', '.xlsx'))
        merged_data.to_excel(output_path, index=False, engine="openpyxl")

    print(f"Consolidated file saved to: {output_path}")


if __name__ == "__main__":
    config = load_config()
    if not config:
        exit()

    source_directory = config.get("join_in_dir")
    output_directory = config.get("join_out_dir")
    output_filename = config.get("output_filename", "joined_file.csv")
    csv_delimiter = config.get("csv_delimiter", ",")

    # Let the user confirm or override the delimiter
    user_delimiter = input(f"Current CSV delimiter is '{csv_delimiter}'. Enter a new delimiter or press Enter to keep it: ").strip()
    if user_delimiter:
        csv_delimiter = user_delimiter

    data_frames = load_files(source_directory, csv_delimiter)
    if data_frames:
        print("\n--- Transforming Data ---")
        transformed_data_frames = validate_and_transform(data_frames)
        merge_files(transformed_data_frames, output_directory, output_filename)