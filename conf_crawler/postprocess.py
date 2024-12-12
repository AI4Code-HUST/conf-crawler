import logging
import os
import re
import json
from tqdm import tqdm

# Configure logging to both a file and the console
if not os.path.exists("./logs"):
    os.makedirs("./logs")
logging.basicConfig(
    force=True,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler("./logs/postprocess.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def dump_jsonl(data, file_path):
    """
    Dumps a list of dictionaries to a JSONL file, with each dictionary as a separate JSON object on a new line.

    Args:
        data (list): A list of dictionaries to be written to the file.
        file_path (str): The path to the output JSONL file.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            # Write each dictionary as a JSON object on a new line
            file.write(json.dumps(item, ensure_ascii=False) + '\n')
            
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

def contains_numberth(string):
    # Regular expression to match numbers greater than 10 with the "th" suffix
    # This pattern matches numbers 11 and greater followed by "th" (e.g., "11th", "59th", "100th", etc.)
    pattern = r'\d{1,2}(?:st|nd|rd|th)'
    match = re.search(pattern, string)
    return bool(match)


def main():
    logging.info("Postprocess")
    
    papers = load_jsonl("./outputs/papers.jsonl")
    logging.info(len(papers))
    
    for paper in tqdm(papers):
        if paper["paper"] == '':
            papers.remove(paper)
            continue
        if contains_numberth(paper["paper"]):
            papers.remove(paper)
            continue
        if 'acm' in paper["paper"].lower() or 'ieee' in paper["paper"].lower():
            papers.remove(paper)
            continue
            
    dump_jsonl(papers, "./outputs/postprocessed-papers.jsonl")

if __name__ == "__main__":
    main()
