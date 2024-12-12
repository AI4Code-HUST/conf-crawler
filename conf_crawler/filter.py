import logging
import os
import json
from constants import KEYWORDS, YEARS

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

def main():
    logging.info("Filter")
    
    papers = load_jsonl("./outputs/papers.jsonl")
    logging.info(len(papers))
    
    filtered_papers = []

    for paper in papers:
        paper_text = paper["paper"].lower()
        matched_set = None
        reasons = []

        for keywords in KEYWORDS:
            matched_keywords = [keyword for keyword in keywords if keyword in paper_text]
            if matched_keywords:
                matched_set = keywords
                reasons.append(matched_keywords)

        if matched_set:
            paper_with_reason = paper.copy()
            paper_with_reason["reasons"] = reasons
            filtered_papers.append(paper_with_reason)
            
    second_filtered_papers = []
    for paper in filtered_papers:
        for year in YEARS:
            if "conference" in paper:
                if year in paper["conference"]:
                    second_filtered_papers.append(paper)
            else:
                if year in paper["volume"]:
                    second_filtered_papers.append(paper)

    dump_jsonl(second_filtered_papers, "./outputs/filtered-papers.jsonl")

if __name__ == "__main__":
    main()
