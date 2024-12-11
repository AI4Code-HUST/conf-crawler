import json

def load_jsonl(file_path):
    """
    Loads data from a JSONL file, where each line is a valid JSON object.

    Args:
        file_path (str): The path to the JSONL file to be read.

    Returns:
        list: A list of dictionaries containing the parsed JSON objects.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Parse the line as a JSON object and append to the list
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()} - {e}")
    return data

def write_markdown(data, output_file):
    """
    Writes data into a Markdown table format.

    Args:
        data (list): A list of dictionaries containing paper information.
        output_file (str): The path to the output Markdown file.

    Returns:
        None
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        # Write the header
        file.write("| Conference | Paper Title | Keywords |\n")
        file.write("|------------|-------------|----------|\n")

        # Write each paper as a row
        for paper in data:
            conference = paper.get("conference", paper.get("journal"))
            title = paper.get("paper", "N/A")
            reasons = "; ".join([", ".join(reason) for reason in paper.get("reasons", [])])
            paper_url = paper.get("paper_url", "#")

            file.write(f"| {conference} | [{title}]({paper_url}) | {reasons} |\n")

if __name__ == "__main__":
    # Load the JSONL data
    input_file = "filtered-output.jsonl"
    output_file = "filtered-papers.md"

    data = load_jsonl(input_file)
    
    # Write to Markdown
    write_markdown(data, output_file)
