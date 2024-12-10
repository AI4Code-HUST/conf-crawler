import logging
import os
import requests
import json
from bs4 import BeautifulSoup
from .constants import CONF_LISTS
from urllib.parse import unquote
from tqdm import tqdm

# Configure logging to both a file and the console
if not os.path.exists("./logs"):
    os.makedirs("./logs")
logging.basicConfig(
    force=True,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler("./logs/main.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def crawl_conferences(url:str) -> list:
    """
    Crawl the given DBLP URL and print the titles of the papers.
    """
    try:
        conf_links = []
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # logging.info(soup.prettify())
        
        confs = soup.find_all('a', class_="toc-link")
        for conf_link in confs:
            conf_links.append(conf_link.get("href"))
            # logging.info(conf_link.get("href"))
        
        return conf_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    
def crawl_journal(url:str) -> list:
    try:
        journal_links = []
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # logging.info(soup.prettify())
        
        volume_links = soup.find_all('a', string=lambda text: text and "Volume" in text)
        for journal_link in volume_links:
            # logging.info(journal_link.string)
            journal_links.append(
                {
                    "journal": journal_link.get("href").split('/')[-2],
                    "volume": journal_link.string,
                    "journal_url": journal_link.get("href")
                }
            )
        return journal_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    
def crawl_paper_conf(url:str) -> list:
    try:
        paper_links = []
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # logging.info(soup.prettify())
        
        scholar_links = soup.find_all('a', href=lambda href: href and "https://scholar.google.com/scholar?q=" in href)
        for scholar_link in scholar_links:
            paper_links.append(scholar_link.get("href"))
            # logging.info(scholar_link.get("href"))
        
        return paper_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

def crawl_paper_journal(url:str) -> list:
    try:
        paper_links = []
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # logging.info(soup.prettify())
        
        scholar_links = soup.find_all('a', href=lambda href: href and "https://scholar.google.com/scholar?q=" in href)
        for scholar_link in scholar_links:
            paper_links.append(scholar_link.get("href"))
        
        return paper_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    
def extract_conf_acronym_and_year(url:str) -> str:
    """
    Extract the conference acronym and year from a given DBLP URL.
    """
    parts = url.split('/')
    conf_and_year = parts[-1].split('.')[0]
    
    return conf_and_year

def extract_title_from_scholar_link(url:str) -> str:
    """
    Extract the conference acronym and year from a given DBLP URL.
    """
    parts = url.split('=')
    title = parts[-1]
    title = title.replace('+', ' ')
    title = unquote(title)

    return title

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

def main():
    logging.info("---Conference Cralwer---")
    
    papers = []
    for conf in tqdm(CONF_LISTS, desc="Processing configurations"):
        if 'conf' in conf:
            conf_links = crawl_conferences(conf)
            for link in conf_links:
                # logging.info(link)
                conf_name = extract_conf_acronym_and_year(link)
                paper_links = crawl_paper_conf(link)
                for paper in paper_links:
                    title = extract_title_from_scholar_link(paper)
                    paper_metadata = {
                        "conference": conf_name,
                        "conf_url": link,
                        "paper": title,
                        "paper_url": paper
                    }
                    papers.append(paper_metadata)
        else:
            conf_links = crawl_journal(conf)
            for link in conf_links:
                paper_links = crawl_paper_journal(link["journal_url"])
                for paper in paper_links:
                    title = extract_title_from_scholar_link(paper)
                    paper_metadata = {
                        "journal": link["journal"],
                        "volume": link["volume"],
                        "journal_url": link["journal_url"],
                        "paper": title,
                        "paper_url": paper
                    }
                    # logging.info(paper_metadata)
                    papers.append(paper_metadata)
            
    dump_jsonl(papers, "output.jsonl")

if __name__ == "__main__":
    main()
