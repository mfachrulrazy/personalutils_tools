import os
import json
import pandas as pd

def read_csv_file(file_path):
    """
        Reads a CSV file and returns a Pandas DataFrame.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
def detect_json_columns(dataframe):
    """
        Detects columns in the DataFrame with JSON-like values.
    """
    json_like_columns = []

    for column in dataframe.columns:
        if dataframe[column].apply(is_json_col).all():
            json_like_columns.append(column)

    return json_like_columns

def is_json_col(value):
    """
        Check if a value of column is JSON-like format
    """
    if pd.isna(value):
        return False
    try:
        json.loads(value)
        return True
    except (TypeError, json.JSONDecodeError):
        return False
    
def process_json_col(dataframe, json_columns):
    """
        Convert JSON-like format columns to Python objects in the DataFrame
    """
    for column in json_columns:
        dataframe[column] = dataframe[column].apply(json.loads)
    return dataframe

def transform_data(dataframe, json_column):
    """
        Transforms the DataFrame to JSON output structure
    """

    transformed_data = []

    for _, row in dataframe.iterrows():
        other_columns = {col: row[col] for col in dataframe.columns if col != json_column}

        # parse JSON-like format column
        json_data = row[json_column]
        if not isinstance(json_data, dict):
            continue

        json_data_transformed = recursively_add_defaults(json_data)

        base_record = {
            **other_columns,
            json_column: json_data_transformed,
        }

        transformed_data.append(base_record)

    return transformed_data

def recursively_add_defaults(json_data, default_value=None):
    """
        Recursively adds default values for missing keys in a JSON-like dictionary or list
    """

    if isinstance(json_data, dict):
        return {
            key: recursively_add_defaults(value, default_value)
            for key, value in json_data.items()
        }
    elif isinstance(json_data, list):
        return [recursively_add_defaults(item, default_value) for item in json_data]
    else:
        return json_data if json_data is not None else default_value
    
def save_to_json(data, output_path):
    """
        Saves the transformed data to a JSON file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Error saving to JSON file: {e}")
    
def convert_csv_to_json(csv_path, json_path):
    """
        Converts a CSV file to a JSON file, processing and transforming all columns including JSON-like format
    """

    print(f"Reading CSV file from: {csv_path}")
    df = read_csv_file(csv_path)

    print("Detecting JSON-like format columns...")
    json_like_columns = detect_json_columns(df)

    if not json_like_columns:
        raise ValueError("No JSON-like format columns detected in the CSV file.")
    
    print(f"Detected JSON-like colum: {json_like_columns[0]}")

    df = process_json_col(df, json_like_columns)
    transformed_data = transform_data(df, json_like_columns[0])

    print(f"Saving JSON to : {json_path}")
    save_to_json(transformed_data, json_path)
    print("Conversion completed successfully.")

if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    input_folder = config.get("csjs_in_dir")
    output_folder = config.get("csjs_out_dir")

    try:
        for file_name in os.listdir(input_folder):
            if file_name.endswith('.csv'):
                input_file = os.path.join(input_folder, file_name)
                output_file = os.path.join(output_folder, file_name.replace('.csv','.json')) 

                print(f"Processing {input_file} ...")
                convert_csv_to_json(input_file, output_file)
                print(f"Saved JSON file to {output_file}")

        print("All files have been processed!")

    except Exception as e:
        print(f"Error: {e}")