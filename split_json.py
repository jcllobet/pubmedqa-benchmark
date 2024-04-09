import json
import os 

def split_json_file(input_file_path, output_prefix, parts=10):
    # Load the original JSON data
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    # Assuming the data is a list for splitting
    if isinstance(data, dict):
        data = list(data.values())
    elif not isinstance(data, list):
        print("This script requires the top-level JSON structure to be a list or a dictionary with list values.")
        return

    # Calculate the size of each part
    total_length = len(data)
    part_size = total_length // parts

    # Split the data and write to separate files
    for part in range(parts):
        start_index = part * part_size
        # For the last part, include any remaining items
        end_index = (part + 1) * part_size if part < parts - 1 else total_length
        part_data = data[start_index:end_index]

        # Construct the output file name
        output_file_path = f"{output_prefix}_part_{part + 1}.json"
        
        # Write the part data to a new JSON file
        with open(output_file_path, 'w') as output_file:
            json.dump(part_data, output_file, indent=4)

        print(f"Part {part + 1} written to {output_file_path}")

# Example usage
current_dir = os.path.dirname(__file__)
input_file_path = os.path.join(current_dir, 'data', 'contexts_pqau.json')
output_prefix = os.path.join(current_dir, 'data', 'contexts_pqau_split')

split_json_file(input_file_path, output_prefix)