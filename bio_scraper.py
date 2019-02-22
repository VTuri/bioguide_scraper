from bs4 import BeautifulSoup
import re

def bio_scrapper(url):
    # Open the link
    soup = BeautifulSoup(open(url))

    # Search for the part where the bio is and get the text
    all_data = soup.find_all('p')
    text = all_data[0].get_text()

    # Create a single line from the text
    text = text.replace('\n', '')

    # Regex to delete all the multiple whitespaces
    re.sub(' +',' ', text)

    return text


