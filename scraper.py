from bs4 import BeautifulSoup
from model import db_connection, bio_scrapper
from urllib.request import urlopen

input_url = 'example_page.html'
soup = BeautifulSoup(open(input_url))

final_link = soup.p.a
final_link.decompose()

# Find the TR blocks which holds the data that we want to retrieve
all_data = soup.find_all('tr')
name_storage = []

for row in range(len(all_data)):
    current_list = []

    # Takes one TR block
    current = all_data[row]

    # Takes the TD part from current TR
    current_tab = current.find_all('td')

    # Creates a list from the different elements in the current tab
    for i in current_tab:
        current_list.append(i.text)

    # Get the link for the current person
    current_link = current.find_all('a')

    # We are not dealing with an empy list
    if len(current_link) > 0:
        current_link = current_link[0].get('href')

        open_link = urlopen(current_link)

        # Create a dictionary about the current person
        name_dict = {'id': current_link[-7:],
                     'first_name': current_list[0].split(',')[0].lower(),
                     'last_name': current_list[0].split(',')[1].strip().lower(),
                     'born': current_list[1][:4],
                     'death': current_list[1][5:],
                     'occupation': current_list[2],
                     'party': current_list[3],
                     'state': current_list[4],
                     'congress_year': current_list[5],
                     'link': current_link,
                     'bio': bio_scrapper(open_link)
                     }

        # Print current ID
        print('ID of completed page: ' + str(name_dict['id']))

        # Add it to the list of names
        name_storage.append(name_dict)

# Final list with all the Congress members based on the search and the link to their bios
# name_storage

# Save the list into a db
db_connection('congress_43.db', name_storage)
