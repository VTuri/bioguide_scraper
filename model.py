from bs4 import BeautifulSoup
import re
import sqlite3


def bio_scrapper(url):
    """Scrape the bio of a given person based on the link that the other scraper provides"""
    # Open the link provided by the main scraper
    soup = BeautifulSoup(open(url))

    # Search for the part where the bio is and get the text
    all_data = soup.find_all('p')
    text = all_data[0].get_text()

    # Create a single line from the text
    text = text.replace('\n', '')

    # Regex to delete all the multiple whitespaces
    re.sub(' +', ' ', text)

    return text


def db_connection(db_name, data):
    """Connect to a db write the data in it and close the connection"""
    # Connect to DB
    conn = sqlite3.connect(db_name)

    # Loop through the data and write it in the db
    for person in data:
        # list_of_values = list(person.values())
        write_db(db_name,person.values())

    # After commit (every change is saved) we close the connection
    conn.close()


def write_db(db_name, data_list):
    data_list = list(data_list)

    person_id = data_list[0]
    first_name = data_list[1]
    last_name = data_list[2]
    born = data_list[3]
    death = data_list[4]
    occupation = data_list[5]
    party = data_list[6]
    state = data_list[7]
    congress_year = data_list[8]
    link = data_list[9]

    # connect to db, default setting = rwc (read/write/create)
    conn = sqlite3.connect(db_name)

    # Create cursor object
    c = conn.cursor()

    # Create a table if it doesnt exist with the columns
    # TODO Add bio if it is implemented
    try:
        c.execute(
            '''CREATE TABLE person (id, first_name, last_name, 
            born, death, occupation, party, state, congress_year, link)''')
    except sqlite3.OperationalError:
        pass

    # Insert a row of data
    c.execute(
        '''INSERT INTO person VALUES (?,?,?,?,?,?,?,?,?,?);''', (
            person_id, first_name, last_name, born, death, occupation, party, state, congress_year, link))
    # Save the changes
    conn.commit()
