import logging
import os
import requests
from bs4 import BeautifulSoup
from .constants import CONF_LISTS

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
            journal_links.append(journal_link.get("href"))
            # logging.info(journal_link.get("href"))
        
        return journal_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

def main():
    logging.info("---Conference Cralwer---")
    
    all_link = []
    for conf in CONF_LISTS:
        if 'conf' in conf:
            all_link += crawl_conferences(conf)
        else:
            all_link += crawl_journal(conf)
        
    all_link = set(all_link)
    # logging.info(all_link)
    
    

if __name__ == "__main__":
    main()
