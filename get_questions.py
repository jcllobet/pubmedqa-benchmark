import json

def get_questions(input_file_path, output_file_path):
    # Load the original JSON data
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    print(type(data))

    # Extract only the question component
    questions = []
    # Check if data is a dictionary and try to extract questions accordingly
    for item in data.values():
        if "QUESTION" in item:  # Check if "QUESTION" key exists in the item
            questions.append(item["QUESTION"])

    # Write the questions to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(questions, output_file, indent=4)

    print(f"Questions written to {output_file_path}")
    # Write the questions to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(questions, output_file, indent=4)

    print(f"Questions written to {output_file_path}")

def get_context(input_file_path, output_file_path):
    # Load the original JSON data
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    print(type(data))

    # Extract only the question component
    contexts = []
    # Check if data is a dictionary and try to extract contexts accordingly
    for item in data.values():
        if "CONTEXTS" in item:  # Check if "QUESTION" key exists in the item
            contexts.append(item["CONTEXTS"])

    # Write the contexts to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(contexts, output_file, indent=4)

    print(f"contexts written to {output_file_path}")
    # Write the contexts to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(contexts, output_file, indent=4)

    print(f"contexts written to {output_file_path}")

# Example usage
input_file_path = 'data/ori_pqau.json'
output_file_path = 'data/contexts_pqau.json'
get_context(input_file_path, output_file_path)