import pandas as pd
import json

def csv_to_json_with_selected_fields(input_csv, output_json, include_fields):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(input_csv)

        filtered_df = df[include_fields]

        # Convert the DataFrame to JSON
        json_data = filtered_df.to_dict(orient="records")

        # Write the JSON data to the output file
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        print(f"JSON file successfully created at {output_json}")
    except KeyError as e:
        print(f"Error: The specified field(s) {e} are not in the CSV.")
    except Exception as e:
        print(f"An error occurred: {e}")

fields_to_include = ["Question", "Details", "Answer", "Short Answer", "Topics"]

csv_to_json_with_selected_fields("../libanswers_faq_export_oct_2024.csv", "../libanswers_export_faq.json", fields_to_include)
