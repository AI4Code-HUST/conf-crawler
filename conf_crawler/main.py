import logging
import os

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

def main():
    logging.info("Hello, world!")

if __name__ == "__main__":
    main()
