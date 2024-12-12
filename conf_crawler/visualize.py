import json
import re

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

def generate_markdown_table(data):
    """
    Generates a Markdown table for the given data.

    Args:
        data (list): A list of dictionaries containing paper information.

    Returns:
        str: A Markdown table as a string.
    """
    table = ["| Conference | Paper Title | Keywords |", "|------------|-------------|----------|"]

    for paper in data:
        conference = paper.get("conference", paper.get("journal"))
        title = paper.get("paper", "N/A")
        reasons = "; ".join([", ".join(reason) for reason in paper.get("reasons", [])])
        paper_url = paper.get("paper_url", "#")

        table.append(f"| {conference} | [{title}]({paper_url}) | {reasons} |")

    return "\n".join(table)

def update_readme_section(readme_path, section_title, new_content):
    """
    Updates a specific section in the README.md file.

    Args:
        readme_path (str): The path to the README.md file.
        section_title (str): The title of the section to update.
        new_content (str): The new content to replace in the section.

    Returns:
        None
    """
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    section_pattern = rf"(?<=## {section_title}\n)(.*?)(?=\n## |\Z)"
    updated_content = re.sub(section_pattern, new_content, readme_content, flags=re.S)

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    # Load the JSONL data
    input_file = "./outputs/filtered-papers.jsonl"
    readme_file = "./README.md"

    data = load_jsonl(input_file)

    # Generate the new Markdown table
    markdown_table = generate_markdown_table(data)

    # Update the ## Papers section in the README
    update_readme_section(readme_file, "Papers", markdown_table)
